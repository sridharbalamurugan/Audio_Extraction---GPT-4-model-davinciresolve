import xml.etree.ElementTree as ET     ## extract workflow from .poml 
import openai              ## run ai prompt using the input video and extracted instructions 


tree = ET.parse('video.pml')
root = tree.getroot()



# Generate subtitles_output (replace this with actual subtitle generation logic)
subtitles_output = "Subtitle line 1\nSubtitle line 2\n"

with open("subtitles.srt","w",encoding="utf-8") as f:   #save to subtitle file.
    f.write(subtitles_output)
