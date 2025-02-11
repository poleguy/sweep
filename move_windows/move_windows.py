import subprocess
import re
import time

def get_monitor_geometry():
    """Retrieve monitor geometries using xrandr."""
    output = subprocess.check_output("xrandr --listmonitors", shell=True, text=True)
    monitors = {}
    for line in output.splitlines():
        match = re.search(r'(\d+)/\d+x(\d+)/\d+\+(\d+)\+(\d+)', line)
        if match:
            width, height, x_offset, y_offset = map(int, match.groups())
            print(width,height,x_offset,y_offset)
            monitors[(x_offset, y_offset)] = (width, height, x_offset, y_offset)
    return monitors # dictionary of width, height, x_offset, y_offset  tuples by x_offset, y_offset keys

def get_windows_on_monitor(monitor_geometry):
    """Find all windows on a specific monitor."""
    mon_width, mon_height, mon_x_offset, mon_y_offset = monitor_geometry

    print(monitor_geometry)
    output = subprocess.check_output("wmctrl -lG", shell=True, text=True)
    windows = []
    print(output)
    for line in output.splitlines():
        parts = line.split()
        if len(parts) < 7:
            continue
        window_id, weight, x, y, width, height = parts[0], int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5])
        if is_window_on_monitor(x,y,width,height,mon_x_offset,mon_y_offset,mon_width,mon_height):
            print(window_id,x,y,width, height, mon_width,mon_height,mon_x_offset,mon_y_offset)
            if weight < 0:
                print(window_id,"weight is too low")
            elif is_window_maximized(window_id):
                print(window_id,"maximized")
            else:
                windows.append(window_id)
    return windows

def move_window_to_monitor(window_id, target_geometry):
    """Move a window to the target monitor."""
    _,_,x_offset, y_offset = target_geometry
    cmd = f"wmctrl -i -r {window_id} -e 0,{x_offset},{y_offset},-1,-1"
    print(cmd)
    subprocess.run(cmd, shell=True)

def move_windows_to_monitor(source_monitor, target_monitor):
    """Move all windows from source monitor to target monitor."""
    windows = get_windows_on_monitor(source_monitor)
    for window in windows:
        move_window_to_monitor(window, target_monitor)

def launch_and_move_application(app_name, target_monitor):
    """Launch an application and move it to the target monitor in fullscreen."""
    # Launch the application
    subprocess.Popen(app_name, shell=True)
    time.sleep(2)  # Wait for the application to open

    # Find the application's window
    output = subprocess.check_output("wmctrl -l", shell=True, text=True)
    for line in output.splitlines():
        if app_name in line:
            window_id = line.split()[0]
            move_window_to_monitor(window_id, target_monitor)
            subprocess.run(f"wmctrl -i -r {window_id} -b add,fullscreen", shell=True)
            break

def move_application(app_name, target_monitor):
    """ move it to the target monitor in fullscreen."""

    # Find the application's window
    output = subprocess.check_output("wmctrl -l", shell=True, text=True)
    for line in output.splitlines():
        print(line)
        if app_name in line:
            window_id = line.split()[0]
            move_window_to_monitor(window_id, target_monitor)
            #subprocess.run(f"wmctrl -i -r {window_id} -b add,fullscreen", shell=True)
            subprocess.run(f"wmctrl -i -r {window_id} -b add,maximized_vert,maximized_horz", shell=True)
            break


def is_window_maximized(window_id):
    """
    Check if a window is maximized based on its _NET_WM_STATE property.

    Args:
        window_id (str): The window ID.

    Returns:
        bool: True if the window is maximized, False otherwise.
    """
    try:
        # Use xprop to get the _NET_WM_STATE of the window
        output = subprocess.check_output(f"xprop -id {window_id} _NET_WM_STATE", shell=True, text=True)

        for line in output.splitlines():
            # Extract the property value
            if "_NET_WM_STATE" in line:
                # Check for maximized states
                if "_NET_WM_STATE_MAXIMIZED_HORZ" in output and "_NET_WM_STATE_MAXIMIZED_VERT" in output:
                    return True
    except subprocess.CalledProcessError:
        print(f"Failed to get _NET_WM_STATE for window {window_id}.")
        
    return False


def is_window_on_monitor(window_x, window_y, window_width, window_height, 
                         monitor_x, monitor_y, monitor_width, monitor_height):
    """
    Check if a window is on a monitor based on their positions and dimensions.

    Args:
        window_x (int): The x-coordinate of the window's top-left corner.
        window_y (int): The y-coordinate of the window's top-left corner.
        window_width (int): The width of the window.
        window_height (int): The height of the window.
        monitor_x (int): The x-coordinate of the monitor's top-left corner.
        monitor_y (int): The y-coordinate of the monitor's top-left corner.
        monitor_width (int): The width of the monitor.
        monitor_height (int): The height of the monitor.

    Returns:
        bool: True if the window is on the monitor, False otherwise.
    """
    # Calculate the boundaries of the window and monitor
    window_right = window_x + window_width
    window_bottom = window_y + window_height
    monitor_right = monitor_x + monitor_width
    monitor_bottom = monitor_y + monitor_height

    # Check if any part of the window is within the monitor's boundaries
    is_within_horizontal = window_x < monitor_right and window_right > monitor_x
    is_within_vertical = window_y < monitor_bottom and window_bottom > monitor_y

    return is_within_horizontal and is_within_vertical


def main():
    monitors = get_monitor_geometry()
    monitor_list = list(monitors.keys())

    if len(monitors) < 2:
        print("Error: At least two monitors are required.")
        return

    print(monitor_list)
    # Define source and target monitors
    source_monitor = monitors[monitor_list[1]]
    target_monitor = monitors[monitor_list[0]]

    # Move windows from source to target
    move_windows_to_monitor(source_monitor, target_monitor)

    # Move specific application (e.g., "firefox") to the target monitor
    app_name = "Krita"
    move_application(app_name, source_monitor)

if __name__ == "__main__":
    main()
