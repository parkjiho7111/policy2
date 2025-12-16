import json
import os

# Configuration
# Source directory
source_directory = r"c:\Users\PC\Desktop\policy2\policy.json"
# Target directory for policies with missing/null aplyYmd
target_directory = r"c:\Users\PC\Desktop\policy2\no_aplyYmd_policies"

if not os.path.exists(target_directory):
    os.makedirs(target_directory)

def filter_and_move_policies():
    files = [f for f in os.listdir(source_directory) if f.endswith(".json")]
    
    total_moved = 0
    total_checked = 0
    
    for filename in files:
        source_filepath = os.path.join(source_directory, filename)
        target_filepath = os.path.join(target_directory, filename)
        
        print(f"Processing {source_filepath}...")
        
        try:
            with open(source_filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if "result" not in data or "youthPolicyList" not in data["result"]:
                print(f"Skipping {filename}: Invalid structure")
                continue
                
            policies = data["result"]["youthPolicyList"]
            original_count = len(policies)
            total_checked += original_count
            
            valid_policies = []
            invalid_policies = []
            
            for p in policies:
                aply_ymd = p.get("aplyYmd")
                
                # Check if aplyYmd is None (null in JSON), empty string, or literally "null" string (just in case)
                if aply_ymd is None or aply_ymd == "" or aply_ymd == "null":
                    invalid_policies.append(p)
                else:
                    valid_policies.append(p)
            
            num_moved = len(invalid_policies)
            total_moved += num_moved
            
            # 1. Update source file with ONLY valid policies
            data["result"]["youthPolicyList"] = valid_policies
            if "pagging" in data["result"]:
                 data["result"]["pagging"]["totCount"] = len(valid_policies)
            
            with open(source_filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                
            # 2. Write invalid policies to the new file in target directory
            # Only creating the file if there are actual invalid policies to move
            if invalid_policies:
                # Structure for new file
                new_data = {
                    "result": {
                        "youthPolicyList": invalid_policies,
                        "pagging": {
                            "totCount": num_moved
                        }
                    }
                }
                
                with open(target_filepath, 'w', encoding='utf-8') as f:
                    json.dump(new_data, f, ensure_ascii=False, indent=4)
                    
            print(f"  Moved {num_moved} policies to {target_directory}. Remaining in source: {len(valid_policies)}")
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print(f"\nProcessing Complete.")
    print(f"Total Checked: {total_checked}")
    print(f"Total Moved: {total_moved}")

if __name__ == "__main__":
    filter_and_move_policies()
