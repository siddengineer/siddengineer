import pandas as pd
import os
from datetime import datetime

def get_file_path():
    now = datetime.now()
    file_name = f'gym_attendance_{now.year}_{now.month:02d}.csv'
    return os.path.join(os.path.dirname(__file__), file_name)

def create_or_load_attendance_sheet():
    file_path = get_file_path()
    if not os.path.exists(file_path):
        # Create a new attendance sheet with days of the current month
        now = datetime.now()
        days_in_month = pd.date_range(start=f'{now.year}-{now.month:02d}-01', end=f'{now.year}-{now.month:02d}-{pd.Timestamp(now).days_in_month:02d}')
        attendance_df = pd.DataFrame({'Date': days_in_month.strftime('%Y-%m-%d')})
        body_parts = ['Chest', 'Back', 'Legs', 'Arms', 'Shoulders', 'Abs']
        for part in body_parts:
            attendance_df[part] = ''
        attendance_df['Present'] = 'No'
        attendance_df.to_csv(file_path, index=False)
    else:
        # Load the existing attendance sheet
        attendance_df = pd.read_csv(file_path)
    return attendance_df

def log_gym_visit(date, body_part):
    attendance_df = create_or_load_attendance_sheet()
    row_index = attendance_df.index[attendance_df['Date'] == date].tolist()
    if row_index:
        row_index = row_index[0]
        if body_part in attendance_df.columns:
            attendance_df.at[row_index, body_part] = 'Yes'
        attendance_df.at[row_index, 'Present'] = 'Yes'
        attendance_df.to_csv(get_file_path(), index=False)
        print(f'Logged: {date} - {body_part}')
    else:
        print(f'Error: Date {date} not found in the attendance sheet.')

def display_attendance():
    attendance_df = create_or_load_attendance_sheet()
    print("\n--- Full Attendance Sheet ---")
    print(attendance_df)

def display_day_attendance(date):
    attendance_df = create_or_load_attendance_sheet()
    if date in attendance_df['Date'].values:
        print(f"\n--- Attendance for {date} ---")
        print(attendance_df[attendance_df['Date'] == date])
    else:
        print(f'Error: Date {date} not found in the attendance sheet.')

if __name__ == '__main__':
    while True:
        choice = input('Do you want to log a gym visit or view data? (log/view/exit): ').strip().lower()
        if choice == 'log':
            date = input('Enter the date (YYYY-MM-DD): ')
            body_part = input('Enter the body part (e.g., Chest, Back, Legs, Arms, Shoulders, Abs): ')
            log_gym_visit(date, body_part)
        elif choice == 'view':
            view_choice = input('View full attendance or a specific day? (full/day): ').strip().lower()
            if view_choice == 'full':
                display_attendance()
            elif view_choice == 'day':
                date = input('Enter the date (YYYY-MM-DD): ')
                display_day_attendance(date)
            else:
                print('Invalid option for viewing.')
        elif choice == 'exit':
            print('Exiting the program.')
            break
        else:
            print('Invalid option, please enter "log", "view", or "exit".')
