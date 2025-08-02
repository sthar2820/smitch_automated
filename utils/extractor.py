
def extract_smitch_data_from_path(file_path):
    from openpyxl import load_workbook
    wb = load_workbook(file_path, data_only=True)
    ws = wb.active

    metric_columns, headers, stop_column_found = detect_metric_columns(ws)
    category_rows = detect_categories(ws)
    subcategory_col = find_subcategory_column(ws, category_rows)
    plant_name, plant_row = detect_plant(ws)
    part_name = detect_part_name(ws, category_rows)

    core_data = extract_smitch_data(ws, category_rows, metric_columns, headers, subcategory_col, plant_name, part_name)
    apw_data = extract_weekly_apw(ws, plant_name, part_name)
    ebit_data = extract_ebit_metrics(ws, plant_name, part_name, category_rows)

    return core_data + apw_data + ebit_data
