# Maya Mirror Pose Plugin
note:- I manually write these "note" lines and "##Installation" block is written by me, rest is AI-generated 

note:- make sure to drag and drop  this command "mirrorPoseUI()" on your shelf tools to pop up the UI(for ease of access)

## Overview
The **Maya Mirror Pose Plugin** is a custom tool for Autodesk Maya that allows animators to mirror the pose of selected controllers with a single click. This tool is especially useful for character rigs with symmetrical controls, facilitating the animation process by automating the mirroring of keyframe values for translation and rotation attributes.

## Features
✔️ Mirroring of translation and rotation values of selected controllers  
✔️ Handles controllers with side-indicating suffixes (`L`, `l`, `R`, `r`)  
✔️ Flips values of center controllers (without side suffixes)  
✔️ User-friendly UI activated via a Maya shelf button  

## Installation
download, save, and run the script below on your Maya script editor

"mirror_pose_ui.py" file 

2. **Add the Shelf Button:**
    - Open `create_shelf_button.mel` in a text editor and replace any placeholder paths with the actual path where your script will be stored.
    - Execute the `create_shelf_button.mel` script in Maya's MEL script editor to create the shelf button.

3. **Install the Plugin Script:**
    - Place `mirror_pose_ui.py` in a directory accessible by Maya.

4. **Load the Plugin:**
    - In Maya's Python script editor, load and run the plugin script:
        ```python
        execfile('path_to_mirror_pose_ui.py')
        ```
      Replace `'path_to_mirror_pose_ui.py'` with the actual path to your `mirror_pose_ui.py` script.

## Usage

1. **Activate the Plugin:**
    - Click the "Mirror Pose" button on the custom shelf to open the plugin UI.

2. **Mirror Poses:**
    - Select the controllers you want to mirror.
    - Click the "Mirror Pose" button in the UI.

## Script Details

### `create_shelf_button.mel`
This script creates a custom shelf button in Maya to activate the mirror pose plugin.

```mel
if (`shelfLayout -exists "CustomShelf"`) {
    shelfButton -parent "CustomShelf" -label "Mirror Pose" -command "mirrorPoseUI" -image1 "commandButton.png";
} else {
    string $shelf = `shelfLayout "CustomShelf"`;
    shelfButton -parent $shelf -label "Mirror Pose" -command "mirrorPoseUI" -image1 "commandButton.png";
}
