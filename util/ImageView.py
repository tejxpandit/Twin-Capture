# File      : Image Viewer Class for DearPyGUI in Python
# Author    : Tej Pandit
# Date      : Oct 2024

import dearpygui.dearpygui as dpg
from util.ImageConvert import ImageConvert

p_offset = 25

class Image:
    def __init__(self):
        # Tags
        self.tag = None
        self.tex = None
        self.parent = None
        self.window = None
        # Properties
        self.img_type = "file"
        self.format = dpg.mvFormat_Float_rgb
        self.width = None
        self.height = None
        self.channels = None
        # Data
        self.data = None
        # Display Config
        self.scale = 1.0

class ImageView:
    def __init__(self, parent=None, texture_registry=None, item_handler_registry=None):
        self.converter = ImageConvert()
        self.images = {}
        self.parents = {}
        self.default_parent = parent
        self.auto_resize = True

        self.tex_reg_tag = texture_registry
        self.item_handler_reg_tag = item_handler_registry
        
        self.initTextureRegistry()
        self.initItemHandlerRegistry()
        self.initAutoResize()

    # Initialize Texture Registry
    def initTextureRegistry(self):
        if self.tex_reg_tag is None:
            self.tex_reg_tag = dpg.add_texture_registry(show=True)

    # Optional : Change Custom/Existing Texture Registry
    def changeTextureRegistry(self, texture_registry_tag):
        self.tex_reg_tag = texture_registry_tag

    # Initialize Item Handler Registry
    def initItemHandlerRegistry(self):
        if self.item_handler_reg_tag is None:
            self.item_handler_reg_tag = dpg.add_item_handler_registry(show=False)
        
    # Initialize Auto-Resize
    def initAutoResize(self):
        dpg.add_item_resize_handler(parent=self.item_handler_reg_tag, callback=self.autoResize)

    # Set Default Parent Container
    def setDefaultParent(self, parent):
        self.default_parent = parent
    
    # Clear Default Parent
    def clearDefaultParent(self):
        self.default_parent = None

    # Set Image Scale
    def setImageScale(self, img, scale):
        img.scale = scale

    # Set Image Max Width
    def setImageWidth(self, img, width):
        img.scale = width / img.width

    # Set Image Max Height
    def setImageHeight(self, img, height):
        img.scale = height / img.height

    # Enable/Disable Auto-Resize
    def enableAutoResize(self, default=True):
        self.auto_resize = default

    # Auto-Resize
    def autoResize(self, item_reg, parent):
        # Check : Auto-Resize Enabled ?
        if self.auto_resize:
            # Check : Parent Exists ?
            if parent is not None:
                # Check : Parent is in Handler Registry ?
                if parent in self.parents:
                    p_width = dpg.get_item_width(parent)
                    # p_height = dpg.get_item_height(parent)
                    for img_tag in self.parents[parent]:
                        # Retrieve Image
                        img = self.images[img_tag]
                        # Calculate Scale w.r.t. Parent Width
                        self.setImageWidth(img, (p_width-p_offset))
                        # Scale Image to Parent Width
                        dpg.configure_item(img.tag, width=img.width*img.scale, height=img.height*img.scale)
                    
    
    # Format Specifier
    def imageFormat(self, channels):
        if channels==3:
            format = dpg.mvFormat_Float_rgb
        else:
            format = dpg.mvFormat_Float_rgba
        return format

    # Create New Image
    def newImage(self, image=None, tag=None, parent=None, img_type="file", scale=1.0, def_width=100, def_height=100, def_channels=3):
        # Create New Image
        img = Image()
        # Initialize Blank Image Defaults
        img.img_type = img_type
        img.width = def_width
        img.height = def_height
        img.channels = def_channels
        img.scale = scale
        # Generate Image Tag (Title)
        img.tag = dpg.generate_uuid()

        # Set Image Parent
        if parent is None:
            if self.default_parent is None:
                img.parent = dpg.generate_uuid()
                window_label = "Image Viewer : " + str(img.tag)
                dpg.add_window(label=window_label, tag=img.parent)
            else:
                img.parent = self.getUUID(self.default_parent)
        else:
            img.parent = self.getUUID(parent)
        # Check for Empty Image
        if image is None:
            # Create Blank Image
            self.blankImage(img)
        else:
            # Convert and Import Image Data
            img.width, img.height, img.channels, img.data = self.converter.imageConvert(image, img_type)
        # Identify Image Format
        img.format = self.imageFormat(img.channels)
        # Add Image Texture to Registry
        img.tex = dpg.add_raw_texture(width=img.width, height=img.height, default_value=img.data, format=img.format, parent=self.tex_reg_tag)
        # Add Image to Parent Container
        dpg.add_image(texture_tag=img.tex, tag=img.tag, parent=img.parent, width=img.width*img.scale, height=img.height*img.scale)
        # Add Alias (if any) to the Image
        if isinstance(tag, str):
            dpg.add_alias(tag, img.tag)

        # Add Image to Parent Association List
        if img.parent in self.parents:
            self.parents[img.parent].append(img.tag)
        else:
            self.parents[img.parent] = [img.tag]
            # Bind New Parents to Resize Registry Handler
            dpg.bind_item_handler_registry(img.parent, self.item_handler_reg_tag)
        # Add Image to Images List
        self.images[img.tag] = img
        # Return Image Tag
        return img.tag
    

    # Update Image
    def updateImage(self, image, tag, img_type=None):
        # Get UUID
        tag = self.getUUID(tag)
        # Retrieve Original Image
        img = self.images[tag]
        # Set Image Type (if any)
        if img_type is not None:
            img.img_type = img_type
        # Convert and Import Image Data
        w, h, c, img.data = self.converter.imageConvert(image, img.img_type)
        print(img.width, w, img.height, h, img.channels, c )
        print(img.format)
        # Check if Image Dims have changed
        if (img.width == w) and (img.height == h) and (img.channels == c):
            # Update Image Data
            dpg.set_value(img.tex, img.data)
            print("same")
        else:
            # Updata Properties and Data
            img.width, img.height, img.channels = w, h, c
            # Replace Image
            self.replaceImage(img)
            print("diff")
        
        
    # Replace Image with Different Image
    def replaceImage(self, img):
        # Preserve Old Alias
        alias = dpg.get_item_alias(img.tag)
        # Preserve Old Position
        idx = self.getPosition(img)
        # Delete Old Texture
        dpg.delete_item(img.tex)
        # Delete Old Image
        dpg.delete_item(img.tag)
        # Recalculate Image Format
        img.format = self.imageFormat(img.channels)
        # Create Replacement Image Texture
        img.tex = dpg.add_raw_texture(width=img.width, height=img.height, default_value=img.data, format=img.format, parent=self.tex_reg_tag)
        # Add Replacement Image
        dpg.add_image(texture_tag=img.tex, tag=img.tag, parent=img.parent, width=img.width*img.scale, height=img.height*img.scale)
        # Update Image Data
        dpg.set_value(img.tex, img.data)
        # Restore Alias (if any) to the Image
        if isinstance(alias, str):
            dpg.add_alias(alias, img.tag)
        # Restore Original Position
        self.restoreOrder(img, idx)
        # Resize Image to Window Automatically
        self.autoResize(None, img.parent)
        

    # Create Placeholder Image Texture
    def blankImage(self, img):
        img.data = [1.0] * (img.width * img.height * img.channels)

    # Delete Image
    def deleteImage(self, tag):
        # Get UUID
        tag = self.getUUID(tag)
        # Retrieve Original Image
        img = self.images[tag]
        # Delete Image Texture
        dpg.delete_item(img.tex)
        # Delete Image Tag
        dpg.delete_item(img.tag)
        # Remove Image from Parent Association List
        self.parents[img.parent].remove(img.tag)
        # Remove Image from Images List
        self.images.pop(img.tag)

    def getUUID(self, tag):
        if isinstance(tag, str):
            tag = dpg.get_alias_id(tag)
        return tag

    def getOrder(self, img):
        return dpg.get_item_children(img.parent, 1)
    
    def getPosition(self, img):
        order = self.getOrder(img)
        idx = order.index(img.tag)
        return idx

    def restoreOrder(self, img, idx):
        order = self.getOrder(img)
        order.remove(img.tag)
        order.insert(idx, img.tag)
        dpg.reorder_items(img.parent, 1, order)

    # TODO : Allow for non-window based parents (groups/tabs), but retain window resizing
    # TODO : Separate base-scale and auto-scale variables

#----------------
# EXAMPLE : USAGE
if __name__ == '__main__': 
    # DPG Context
    dpg.create_context()
    # DPG Viewport
    dpg.create_viewport(title="Image Viewer", width=600, height=300)
    # DPG Window
    dpg.add_window(label="Image Viewer", tag="img_view")

    # DPG Image Viewer Example
    ImgViewer = ImageView(parent="img_view")
    testimg = ImgViewer.newImage("TestImage.png")
    ImgViewer.updateImage("TestImage2.png", testimg)

    # DPG Render Context
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()