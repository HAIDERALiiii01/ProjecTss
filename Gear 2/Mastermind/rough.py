# # # text = "W W W W"
# # # text_list = list(text.replace(" ",""))
# # # for li in text_list:
# # #     print(li)

# # # import time

# # # def countdown(seconds):
# # #     for i in range(seconds, -1, -1):
# # #         mins, secs = divmod(i, 60)
# # #         timer = f"{mins:02d}:{secs:02d}"
# # #         print(f"\r⏳ Time left: {timer}", end="", flush=True)  # overwrite same line
# # #         time.sleep(1)
# # #     print("\r⏰ Time's up!       ", end="", flush=True) 
# # #     times_up = True

# # # # Example: 1 minute 30 seconds
# # # countdown(90)

# # # import time 
# # # from threading import Thread

# # # def task(name):
# # #     for i in range(3):
# # #         print(f"{name} step{i}")
# # #         time.sleep(1)

# # # t1 = Thread(target=task, args=("A",))
# # # t2 = Thread(target=task, args=("B",))

# # # t1.start()
# # # t2.start()

# # # t1.join()
# # # t2.join()

# # import random

# # def mind():
# #     colors = ["R","Y","G"]
# #     box = random.choices(colors, k=5)
# #     print(box)

# # mind()


# # u = input("ENter: ")
# # ll = u.split()
# # print(ll)

# import threading
# import time
# import sys
# import datetime

# # --- Global State ---
# # Flag to signal the timer thread to stop
# stop_timer_flag = threading.Event()
# timer_duration = 30 # Set a duration for the timer in seconds

# def format_time(seconds):
#     """Converts seconds to HH:MM:SS format."""
#     return str(datetime.timedelta(seconds=round(seconds)))

# def run_timer():
#     """
#     Function executed in a separate thread.
#     It updates the timer and redraws the input prompt.
#     """
#     start_time = time.monotonic()
    
#     # 1. Print the static "Timer:" label first
#     sys.stdout.write("Timer: --:--:-- \n")
#     sys.stdout.flush()
    
#     while not stop_timer_flag.is_set() and time.monotonic() < start_time + timer_duration:
#         elapsed = time.monotonic() - start_time
#         remaining = timer_duration - elapsed
#         time_str = format_time(remaining)
        
#         # 2. Move the cursor UP one line (\033[F)
#         # 3. Use carriage return (\r) to go to the start of the line
#         # 4. Clear the line (\033[K) and write the new time
#         # NOTE: These ANSI escape codes (\033[F and \033[K) work on most modern terminals.
        
#         sys.stdout.write(f"\033[F\r\033[KTimer: {time_str} remaining. | Main Status: Running...")
#         sys.stdout.flush()
        
#         # 5. Move the cursor DOWN one line (\n) to return to the input area
#         sys.stdout.write("\n")
#         sys.stdout.flush()
        
#         time.sleep(0.1) # Update frequency
    
#     # Final cleanup after the timer stops
#     if not stop_timer_flag.is_set(): # If timer finished naturally
#         sys.stdout.write("\033[F\r\033[KTimer: 0:00:00. Time's up!      \n")
#     else: # If timer was stopped by external signal (e.g., KeyboardInterrupt)
#         sys.stdout.write("\033[F\r\033[KTimer: Stopped.                  \n")
#     sys.stdout.flush()

# def main_program():
#     """
#     The main program that runs concurrently, taking input.
#     """
#     print("\n--- Input and Calculation Area ---")
    
#     while not stop_timer_flag.is_set():
#         try:
#             # Taking input blocks execution, but the timer thread is still running
#             user_input = input("Enter a number for calculation (or 'q' to quit): ")
            
#             if user_input.lower() == 'q':
#                 print("Quitting main program...")
#                 break
                
#             # --- Performing Calculation ---
#             try:
#                 number = float(user_input)
#                 result = number ** 2
#                 # Print results. The timer is running ABOVE this line.
#                 print(f"Calculation Result: {user_input} squared is {result}")
#             except ValueError:
#                 print("Invalid input. Please enter a number or 'q'.")
            
#         except EOFError: # Handles Ctrl+D/Z
#             print("\nEOF received. Quitting main program...")
#             break
#         except KeyboardInterrupt: # Handles Ctrl+C
#             print("\nKeyboard interrupt received. Quitting main program...")
#             break

# # --- Execution ---

# # 1. Create and start the timer thread
# timer_thread = threading.Thread(target=run_timer)
# timer_thread.daemon = True # Allows the main program to exit even if the timer thread is still running (though we'll join it)
# timer_thread.start()

# try:
#     # 2. Run the main program (input loop)
#     main_program()

# finally:
#     # 3. Signal the timer thread to stop gracefully
#     stop_timer_flag.set()
    
#     # 4. Wait for the timer thread to finish (for clean terminal exit)
#     # Give it a short timeout in case of unexpected hang
#     timer_thread.join(timeout=0.5) 
    
#     print("Program finished.")
import random

elements = ["R", "Y", "G"]
box = random.choices(elements, k=5)
user_input = input("Now guess the set of 5: ")
user_box = user_input.split(",")
if len(user_box) > 5:
    print("Box limit reached")
print(user_box)