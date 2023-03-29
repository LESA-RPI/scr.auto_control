import libtmux
import os
import sys

def run_tmux_auto_control():
    try:
        # Connect to the tmux server or create a new one
        server = libtmux.Server()

        # Create a new session named 'auto_control'
        session_name = 'auto_control'
        if server.has_session(session_name):
            print("Session '{}' already exists. Killing it and creating a new one.".format(session_name))
            server.kill_session(session_name)

        session = server.new_session(session_name)

        # Run 'auto_control.py' in the 'auto_control' session
        window = session.attached_window
        pane = window.attached_pane
        pane.send_keys('python {0}'.format(os.path.abspath("auto_control.py")))

        print("auto_control.py is running in tmux session: '{}'.".format(session_name))
        print("View session using tmux a -t auto_control")
    except Exception as e:
        sys.stderr.write("Error: {}\n".format(e))
        sys.exit(1)

if __name__ == "__main__":
    run_tmux_auto_control()
