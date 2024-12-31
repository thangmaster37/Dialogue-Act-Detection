import os
import json
import argparse
from absl import app

parser = argparse.ArgumentParser(description='S2S')
parser.add_argument('--output_folder_name', type=str, default='utterance_dialogue_data', help='Output folder name')

args = parser.parse_args()

# Hàm trích xuất (x, y) từ các tệp trong một thư mục
def extract_samples_from_dir(data_dir, dialogue_acts_path):

    utterance_dialogue_data = []
    # Load dialogue acts
    with open(dialogue_acts_path, "r") as f:
        dialogue_acts = json.load(f)

    # Lấy danh sách các tệp JSON trong thư mục
    dialogue_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".json")]

    try:
        # Trích xuất (utterance, dialogue act)
        for file in dialogue_files:
            with open(file, "r") as f:
                dialogues = json.load(f)
                for dialogue in dialogues:
                    acts = dialogue_acts[dialogue["dialogue_id"]]
                    for turn in dialogue["turns"]:
                        utterance = turn["utterance"]
                        turn_id = turn["turn_id"]
                        act = acts.get(turn_id).get("dialog_act", {})  # Dialogue act tương ứng
                        utterance_dialogue_data.append(
                            {
                                'utterance': utterance,
                                'dialogue_acts': act
                            }
                        )
        return utterance_dialogue_data
    except Exception as e:
        print("Occurred error:", e)

# Trích xuất dữ liệu và lưu vào file json
def write_data(data_dir, name_dataset, dialogue_acts_path, output_dir):

    # Trích xuất dữ liệu
    dataset = extract_samples_from_dir(data_dir, dialogue_acts_path)

    with open(os.path.join(output_dir, f"{name_dataset}.json"), "w") as f:
        json.dump(dataset, f, indent=2)

def main():

    # Đường dẫn đến thư mục chứa dữ liệu
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    raw_data = os.path.join(BASE_DIR, 'raw_data')

    output_name = args.output_folder_name

    output_path = os.path.join(BASE_DIR, output_name)

    os.makedirs(output_path, exist_ok=True)
    
    # Đường dẫn đến tệp dialogue_acts.json
    dialogue_acts_path = os.path.join(raw_data, "dialog_acts.json")

    train_dir = os.path.join(raw_data, "train")
    val_dir = os.path.join(raw_data, "val")
    test_dir = os.path.join(raw_data, "test")

    write_data(train_dir, 'train', dialogue_acts_path, output_path)
    write_data(test_dir, 'test', dialogue_acts_path, output_path)
    write_data(val_dir, 'val', dialogue_acts_path, output_path)

    print("Data extraction completed.")


if __name__ == "__main__":
    app.run(main())
    
    
