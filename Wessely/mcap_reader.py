import io
import os
import json
import time
import csv
from typing import Optional

import mcap.reader
import mcap.summary
import numpy as np
from pathlib import Path
from mcap.reader import make_reader


class McapTopic:
    def __init__(self, reader: mcap.reader.McapReader, mcap_path: Path, topic_key: int):
        self._reader = reader
        self._mcap_path = mcap_path
        self._mcap_folder = mcap_path.parent
        self._numpy_dir = self._mcap_folder / "numpy"
        self._topic_key = topic_key
        self._topic = self._reader.get_summary().channels[topic_key].topic
        self._message_count = reader.get_summary().statistics.channel_message_counts[topic_key]
        self._schema = json.loads(reader.get_summary().schemas[topic_key].data.decode('utf-8'))
        self._fields = [x.replace(".", "_") for x in self._schema['properties'].keys()]
        self._dtypes = [x['type'] for x in self._schema['properties'].values()]
        self._field_dtypes = {k: v for k, v in zip(self._fields, self._dtypes)}
        self._np_dtype = {'integer': np.int64, 'number': np.float64, 'boolean': np.bool_, "string": "S80", "array": np.float64}

    def get_fields(self):
        return self._fields

    def get_dtypes(self):
        return self._dtypes

    def get_message_count(self):
        return self._message_count

    def _load_data_npy(self):
        np_file = self._numpy_dir / (self._topic + ".npy")

        if os.path.exists(np_file):
            with open(np_file, 'rb') as f:
                return np.load(f)

        return None

    def get_data_list(self):
        """
        Returns its topic data as a dictionary of python lists.
        """
        list_data = {}
        np_data = self.get_data()
        print("Converting to list...", end="")
        transposed_data = np.vstack([np_data[x] for x in np_data.dtype.names])
        for idx, fieldname in enumerate(np_data.dtype.names):
            list_data[fieldname] = transposed_data[idx].tolist()
        print(" finished.")
        return list_data

    def get_data_list_old(self):
        data = {x: [0] * self._message_count for x in self._fields}
        data['ts'] = [0] * self._message_count

        # counts messages
        cnt = 0

        # modulo value to update progress indicator
        mod = int(max(self._message_count / 100, 1))

        # iterate messages up to num_messages
        for schema, channel, message in self._reader.iter_messages(topics=[self._topic]):
            # parse json data
            data_dict = json.loads(message.data.decode('utf-8'))

            # store timestamp
            data['ts'][cnt] = message.publish_time

            # store fields
            for k, v in data_dict.items():
                data[k][cnt] = v

            # increment processed message count
            cnt += 1

            # print progress
            if cnt % mod == 0:
                percent_str = str(int((cnt / self._message_count) * 100)) + "%"
                print("\rLoading " + self._topic + ": " + percent_str, end="")

        # print finished loading
        print("\rLoading " + self._topic + ": 100%")

        # return data dict
        return data

    def get_default_data(self, np_struct_format):
        """
        The default method to convert mcap data into numpy array data.
        """
        data = np.zeros((self._message_count,), dtype=np_struct_format)

        # counts messages
        cnt = 0

        # modulo value to update progress indicator
        mod = int(max(self._message_count / 100, 1))

        # iterate messages up to num_messages
        for schema, channel, message in self._reader.iter_messages(topics=[self._topic]):
            # parse json data
            data_dict = json.loads(message.data.decode('utf-8'))

            # store timestamp
            data['ts'][cnt] = message.publish_time

            # store fields
            for k, v in data_dict.items():
                if self._field_dtypes[k] == "number" and isinstance(v, str):
                    data[k][cnt] = 0
                else:
                    data[k][cnt] = v

            # increment processed message count
            cnt += 1

            # break if num messages have been stored
            if cnt >= self._message_count:
                break

            # print progress
            if cnt % mod == 0:
                percent_str = str(int((cnt / self._message_count) * 100)) + "%"
                print("\rLoading " + self._topic + ": " + percent_str, end="")

        return data

    def get_oscilloscope_data(self, np_struct_format):
        """
        A method to convert oscilloscope mcap data into numpy array data.
        The data must be shaped in the following strucure and must have the following keys:
            rel_time [array] (The relative time since the oscilloscope window started)
            data1 [array]
            dataX... (as many data arrays per window of the same size)
        """
        window_size = 1
        # Get size of the first window to use for all windows in topic
        for schema, channel, message in self._reader.iter_messages(topics=[self._topic]):
            decoded_data = json.loads(message.data)
            window_size = len(decoded_data["rel_time"])
            break
        data_size: int = self._message_count * window_size
        data = np.zeros((data_size,), dtype=np_struct_format)

        # counts messages
        cnt = 0

        # modulo value to update progress indicator
        mod = int(max(self._message_count / 100, 1))

        # iterate messages up to num_messages
        for schema, channel, message in self._reader.iter_messages(topics=[self._topic]):
            # parse json data
            data_dict = json.loads(message.data.decode('utf-8'))
            data_len = len(data_dict["rel_time"])

            # Correctly store all data types and correct publish_time with relative time of data in window
            for i in range(data_len):
                for k, v in data_dict.items():
                    data["ts"][cnt * window_size + i] = message.publish_time + data_dict["rel_time"][i]
                    if type(data_dict[k]) is list:
                        data[k][cnt * window_size + i] = data_dict[k][i]
                    else:
                        data[k][cnt * window_size + i] = data_dict[k]

            # increment processed message count
            cnt += 1

            # break if num messages have been stored
            if cnt >= self._message_count:
                break

            # print progress
            if cnt % mod == 0:
                percent_str = str(int((cnt / self._message_count) * 100)) + "%"
                print("\rLoading " + self._topic + ": " + percent_str, end="")

        return data

    def get_data(self):
        # try to load cached data from disk
        temp_data = self._load_data_npy()

        # return given cached data
        if temp_data is not None:
            print("Loading " + self._topic + ": 100% (cached numpy file)")
            return temp_data

        # create numpy structured array holding fields and timestamp
        np_struct_format = [(x[0], self._np_dtype[x[1]]) for x in zip(self._fields, self._dtypes)]
        np_struct_format.append(('ts', np.uint64))

        # Remove duplicate ts field if present in mcap schema
        ts_fields = []
        for idx, field in enumerate(np_struct_format):
            if field[0] == "ts":
                ts_fields.append(idx)
        if len(ts_fields) > 1:
            np_struct_format.pop(ts_fields[0])

        if "oscilloscope" in self._topic:
            data = self.get_oscilloscope_data(np_struct_format)
        else:
            data = self.get_default_data(np_struct_format)

        # print finished loading
        print("\rLoading " + self._topic + ": 100%")

        # create numpy file path for topic
        np_file = self._numpy_dir / (self._topic + ".npy")

        # create numpy folder if not exists
        if not os.path.exists(self._numpy_dir):
            os.mkdir(self._numpy_dir)

        # store numpy data for topic as numpy file
        with open(np_file, 'wb') as f:
            np.save(f, data)

        # return data dict
        return data


class McapReader:
    def __init__(self):
        self._mcap_file: Optional[io.BufferedReader] = None
        self._reader: Optional[mcap.reader.McapReader] = None
        self._mcap_topics = {}
        self._topic_lut = {}
        self._mcap_path = None

    def open(self, mcap_path: str):
        self._mcap_path = Path(mcap_path)
        self._mcap_file = open(self._mcap_path, "rb")
        self._reader = make_reader(self._mcap_file)

        for k, v in self._reader.get_summary().channels.items():
            try:
                self._mcap_topics[k] = McapTopic(self._reader, self._mcap_path, k)
                self._topic_lut[v.topic] = k
            except KeyError:
                print(f"[Warning] Empty topic {v.topic} found.")

    def close(self):
        if self._mcap_file is not None:
            self._mcap_file.close()
            self._reader = None

    def get_topics(self):
        return [x.topic for x in self._reader.get_summary().channels.values()]

    def get_total_message_count(self):
        return self._reader.get_summary().statistics.message_count

    def get_data_list(self, topic: str):
        return self._mcap_topics[self._topic_lut[topic]].get_data_list()

    def get_data(self, topic: str):
        return self._mcap_topics[self._topic_lut[topic]].get_data()

    def print_info(self):
        info = "MCAP Info:\n"
        info += "  Total Messages: " + str(self.get_total_message_count()) + "\n"
        info += "  Topics:\n"

        for topic in self.get_topics():
            try:
                t = self._mcap_topics[self._topic_lut[topic]]
                info += "    " + topic + ":\n"
                info += "      Messages: " + str(t.get_message_count()) + "\n"
                info += "      Fields: " + str(t.get_fields()) + "\n"
                info += "      Types: " + str(t.get_dtypes()) + "\n"
            except KeyError:
                info += "    " + topic + ":\n"
                info += "      Messages: 0\n"

        print(info)



if __name__ == '__main__':
    # Absolute path to your .mcap file
    file_path = r"C:\Users\TomiNordi2m\OneDrive - i2m Unternehmensentwicklung GmbH\Documents\E-Flex\merged_data\combined_ShellyPro3EM.mcap"

    # Open MCAP file and print info
    mcap_reader = McapReader()
    mcap_reader.open(file_path)
    mcap_reader.print_info()

    import csv
    import os
    import datetime

    # Output folder
    output_dir = r"C:\Users\TomiNordi2m\OneDrive - i2m Unternehmensentwicklung GmbH\Documents\E-Flex\converted_csv"
    os.makedirs(output_dir, exist_ok=True)

    # Loop through all available topics
    for topic_name in mcap_reader.get_topics():
        print(f"\nProcessing topic: {topic_name}")
        module_data = mcap_reader.get_data(topic_name)

        output_file = os.path.join(output_dir, topic_name.replace("/", "_") + ".csv")

        # Remove file if it exists
        if os.path.exists(output_file):
            os.remove(output_file)

        with open(output_file, "w", newline="") as f:
            writer = csv.writer(f)

            # Header: add readable timestamp at the beginning
            headers = list(module_data.dtype.names)
            headers.insert(0, "timestamp")
            writer.writerow(headers)

            written_slots = set()

            for row in module_data:
                ts_ns = row["ts"]
                ts_s = ts_ns / 1e9
                dt = datetime.datetime.fromtimestamp(ts_s)

                # Round down to nearest 15-minute interval
                floored_minute = dt.minute - (dt.minute % 15)
                slot_time = dt.replace(minute=floored_minute, second=0, microsecond=0)

                if slot_time in written_slots:
                    continue  # skip if this slot already written

                # Write row
                row_list = list(row)
                row_list.insert(0, slot_time.strftime("%Y-%m-%d %H:%M"))
                writer.writerow(row_list)
                written_slots.add(slot_time)

        print(f"✅ CSV saved: {os.path.abspath(output_file)}")




    # Close reader
    mcap_reader.close()
