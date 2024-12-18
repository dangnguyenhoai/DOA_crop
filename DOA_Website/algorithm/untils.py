from algorithm.Data import crop_list
def find_crop_id(crop_id, crop_list):
    return next((cay for cay in crop_list if cay["crop_id"] == crop_id),None)
def valid_individual(individual): 
    individual_t = [a.copy() for a in individual]
    land_dict = []
    
    # Initialize land_dict with the first crop of each land
    for i, land_clist in enumerate(individual_t):
        crop_id = land_clist.pop(0)
        crop_month = next(item["crop_month"] for item in crop_list if item["crop_id"] == crop_id)
        land_dict.append({"crop_id": crop_id, "process_month": round(crop_month, 1)})

    # Check for valid conditions
    if len(set(land["crop_id"] for land in land_dict)) != len(land_dict):
        return False
    
    while any(len(land_clist) > 0 for land_clist in individual_t):
        # Find the minimum process_month value
        min_month = min(land["process_month"] for land in land_dict)
        if min_month <= 0:  # Prevent invalid states
            return True
        
        # Subtract the minimum process_month from all lands
        for land in land_dict:
            land["process_month"] = round(land["process_month"] - min_month, 1)

        # Update lands where process_month == 0
        for i, land in enumerate(land_dict):
            if land["process_month"] == 0:
                if len(individual_t[i]) > 0:  # Check if there are crops left
                    new_crop_id = individual_t[i].pop(0)
                    new_crop_month = next(item["crop_month"] for item in crop_list if item["crop_id"] == new_crop_id)
                    land["crop_id"] = new_crop_id
                    land["process_month"] = round(new_crop_month, 1)
        
        # Check if the condition of unique crop IDs is violated
        if len(set(land["crop_id"] for land in land_dict)) != len(land_dict):
            return False

    return True