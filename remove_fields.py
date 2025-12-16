import json
import os

# Configuration
# "All data" - let's process both the main folder and the extracted folder to be thorough, 
# or just the main one. The user said "policy.json 폴더안의..." previously, but now says "all data".
# I'll include the main directory.
directories = [
    r"c:\Users\PC\Desktop\policy2\policy.json",
    r"c:\Users\PC\Desktop\policy2\상시운영정책"
]

fields_to_remove = [
    "sprtArvlSeqYn",
    "sprtTrgtMinAge",
    "sprtTrgtMaxAge",
    "sprtTrgtAgeLmtYn",
    "mrgSttsCd",
    "earnCndSeCd",
    "earnMinAmt",
    "earnMaxAmt",
    "earnEtcCn",
    "bscPlanCycl",
    "bscPlanPlcyWayNo",
    "bscPlanFcsAsmtNo",
    "bscPlanAsmtNo",
    "pvsnInstGroupCd",
    "plcyPvsnMthdCd",
    "plcyAprvSttsCd"
]

def remove_fields():
    for directory in directories:
        if not os.path.exists(directory):
            print(f"Directory not found (skipping): {directory}")
            continue
            
        print(f"Processing directory: {directory}")
        files = [f for f in os.listdir(directory) if f.endswith(".json")]
        
        for filename in files:
            filepath = os.path.join(directory, filename)
            # print(f"  Processing {filename}...")
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "result" not in data or "youthPolicyList" not in data["result"]:
                    # print(f"    Skipping {filename}: Invalid structure")
                    continue
                    
                policies = data["result"]["youthPolicyList"]
                modified = False
                
                for p in policies:
                    for field in fields_to_remove:
                        if field in p:
                            del p[field]
                            modified = True
                
                if modified:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    print(f"  Updated {filename}")
                else:
                    print(f"  No changes needed for {filename}")
                    
            except Exception as e:
                print(f"  Error processing {filename}: {e}")

    print("\nField removal complete.")

if __name__ == "__main__":
    remove_fields()
