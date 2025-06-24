# Maya Batch Shader Creation

Hi, this is the Texture Search and Import tool!

This project was made to simplify the creation of shaders from images in the sourceimages folder of your maya project. The tool will prompt you with the question of which of the identified shaders you want to create and make all the nodes necessary for lookdev in maya for the selected materials.

I was first promped to create this tool by my friend Murat as he found the task of creating shaders and color correction nodes and placing the correct color space, UDIM config, etc repetitive. After some iteration we arrived to this solution, if you have any recommendations they would be greatly appreciated!

# Tool
https://github.com/user-attachments/assets/1cb29d24-a2c8-4a4d-8eb0-1d310d12fccf

Basic usage of the tool, it finds matching naming groups, prompts the user to discard the unwanted ones, creates the rest. The tool also tells you which textures were found and connected afterwards.

https://github.com/user-attachments/assets/43cbef46-9ae3-4025-b7fc-1f642c9ceb2e

It automatically assigns the correct colorspace, UDIMs and color correction nodes ready for lookdev.

If you like the tool, make sure to visit my artstation to see my other projects.
https://www.artstation.com/moises-cg

# Instalation
        Drag and drop the 'install.py' to the maya viewport
        All done! Now you can click the shelf button to use the tool
        A shelf called 'MoisesTools' will be created and you can access the tool from there.

# Usage
        The tool is meant to be used with correct naming conventions. 
        Once you have placed all your images in the sourceimages folder the tool will be able to find 
        them and match them by name, group them and create shaders for all of the different texture names it finds.
        You still have to assign the created materials to the correct mesh, but all the work of placing the nodes 
        and color correction nodes for lookdev is simplified!

# Feedback and Bug Reports

I hope you like the tool and find it useful! If any errors arise or you have any recommendation for the tool's improvement, I would be very happy to hear it. You can always message me in LinkedIn: https://www.linkedin.com/in/moises-cg/


