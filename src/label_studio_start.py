import os
import subprocess


def start_label_studio(port=8080):
    try:
        command = ["label-studio", "start", "--port", str(port)]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        print(f"Label Studio server started on port {port}. PID: {process.pid}")
        print("You can access it in your browser at http://localhost:{}".format(port))
        print("To stop Label Studio, you might need to manually kill the process or implement a shutdown mechanism.")

        return process

    except FileNotFoundError:
        print("Error: 'label-studio' command not found. Make sure Label Studio is installed and in your PATH.")
        print("You can install it using: pip install label-studio")
        return None
    except Exception as e:
        print(f"An error occurred while starting Label Studio: {e}")
        return None

if __name__ == "__main__":
    os.environ['LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED'] = 'true'
    ls_process = start_label_studio(port=8080)

    if ls_process:
        try:
            input("Press Enter to stop Label Studio (if running in this console)...")
        except KeyboardInterrupt:
            print("\nStopping Label Studio process...")
        finally:
            if ls_process.poll() is None:
                ls_process.terminate()
                ls_process.wait(timeout=5)
                if ls_process.poll() is None:
                    ls_process.kill()
                print("Label Studio process terminated.")
    else:
        print("Failed to start Label Studio.")