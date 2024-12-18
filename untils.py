from Data import crop_list
def find_crop_id(crop_id):
    return next((cay for cay in crop_list if cay["crop_id"] == crop_id),None)
def valid_condition(individual):
    individual_t = [a.copy() for a in individual]
    land_dict = []
    # Process
    for i, land_clist in enumerate(individual_t):
        crop_id = land_clist.pop(0)
        crop_month = next(item["crop_month"] for item in crop_list if item["crop_id"] == crop_id)
        land_dict.append({"crop_id": crop_id, "process_month": crop_month})
    # Check is valid condition
    if len(set(land["crop_id"] for land in land_dict)) != len(land_dict):
        return False
    else:
        while any(len(land_clist) > 0 for land_clist in individual_t):
            # Find min process_month value
            min_month = min(land["process_month"] for land in land_dict)

            # Subtract min process_month value to process_month
            for land in land_dict:
                land["process_month"] -= min_month

            # Update new crop if process month  = 0
            for i, land in enumerate(land_dict):
                if land["process_month"] == 0 and len(individual_t[i]) > 0:
                    new_crop_id = individual_t[i].pop(0)
                    new_crop_month = next(item["crop_month"] for item in crop_list if item["crop_id"] == new_crop_id)
                    land["crop_id"] = new_crop_id
                    land["process_month"] = new_crop_month
            # Check is valid condition
            if len(set(land["crop_id"] for land in land_dict)) != len(land_dict):
                return False
    return True