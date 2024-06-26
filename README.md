# BeatGrid

BeatGrid is an interactive music sequencing application that allows users to create and play musical patterns using a grid interface. The application supports loading custom sounds, adjusting playback speed (BPM), recording sessions, and saving/loading patterns.

## Features

- Interactive grid-based music sequencer
- Load custom sounds (WAV/MP3)
- Adjust playback speed (BPM)
- Record and save sessions as MP3 files
- Save and load grid patterns
- Pitch control for each row

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Ladyk3000/beatgrid.git
    ```

2. Navigate to the project directory:
    ```sh
    cd beatgrid
    ```

3. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```sh
    python main.py
    ```

2. Load your sound files into the specified directory.

3. Use the grid interface to create your musical patterns:
    - Click on grid cells to assign sounds.
    - Use the controls to start/stop playback and recording.
    - Adjust the BPM and pitch for each row as needed.
    - Save and load your patterns using the respective buttons.

## Project Structure

- `main.py`: Entry point of the application.
- `music_track_window.py`: Contains the `MusicTrackWindow` class.
- `sound_manager.py`: Handles sound-related operations.
- `ui_components.py`: Contains UI components.
- `cell.py`: Defines the `Cell` class.
- `requirements.txt`: Lists project dependencies.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements, bug fixes, or other improvements.
