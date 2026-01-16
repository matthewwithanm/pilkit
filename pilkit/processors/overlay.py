from pilkit.lib import Image


class ColorOverlay(object):
    """
    Overlay a color mask with a the given opacity
    """

    def __init__(self, color, overlay_opacity=0.5):
        """
        :pamra color: `ImageColor` instance to overlay on the original image
        :param overlay_opacity: Define the fusion factor for the overlay mask

        """
        self.color = color
        self.overlay_opacity = overlay_opacity

    def process(self, img):
        original = img = img.convert('RGB')
        overlay = Image.new('RGB', original.size, self.color)
        mask = Image.new('RGBA', original.size, (0,0,0,int((1.0 - self.overlay_opacity)*255)))
        img = Image.composite(original, overlay, mask).convert('RGB')
        return img


class ImageOverlay(object):
    """
    Overlay an image (i.e watermark) with a given opacity over the original image.
    """

    def __init__(self, overlay_img, position=(0,0)):
        """
        :param overlay_img: PIL `Image` instance to overlay on the original image
        :param position: coordinate (x,y) of the top left corner of the overlay image on the original image. 
        """
        self.overlay_img=overlay_img
        self.position=position
        
    def process(self, img):
        #create the mask (image of same dimension as the original, with the overlay at the right location, with the given opacity)
        mask = Image.new("RGBA",(img.width, img.height),(0,0,0,0)) #transparent image with the same dimensions as original image
        mask.paste(self.overlay_img, (self.position[0], self.position[1])) #put the overlay image at the computed location

        #render the picture overlayed
        if img.mode != "RGBA" :
            tmp = Image.alpha_composite(img.convert("RGBA"), mask) #apply the overlay (both images need to be in "RGBA" mode with alpha_composite())
            img = tmp.convert(img.mode) #convert back to the original mode
        else :
            img = Image.alpha_composite(img, mask)
        return img