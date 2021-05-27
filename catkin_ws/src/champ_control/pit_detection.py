########################################################################
#
# Copyright (c) 2021, STEREOLABS.
#
# All rights reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################
"""
    This sample demonstrates how to capture a live 3D point cloud
    with the ZED SDK and display the result in an OpenGL window.
"""
import sys
import ogl_viewer.viewer as gl
import pyzed.sl as sl
import cv2
from tempfile import TemporaryFile
import numpy as np
if __name__ == "__main__":
    print("Running Depth Sensing sample ... Press 'Esc' to quit")
    init = sl.InitParameters(camera_resolution=sl.RESOLUTION.HD720,
                                 depth_mode=sl.DEPTH_MODE.ULTRA,
                                 coordinate_units=sl.UNIT.METER,
                                 coordinate_system=sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP)
    zed = sl.Camera()
    status = zed.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()
    res = sl.Resolution()
    res.width = 720
    res.height = 1280
    camera_model = zed.get_camera_information().camera_model
    # Create OpenGL viewer
    #viewer = gl.GLViewer()
    #viewer.init(len(sys.argv), sys.argv, camera_model, res)
    point_cloud = sl.Mat(res.width, res.height, sl.MAT_TYPE.F32_C4, sl.MEM.CPU)
    image = sl.Mat(res.width, res.height, sl.MAT_TYPE.F32_C4, sl.MEM.CPU)
    depth = sl.Mat()
    image_zed = sl.Mat(res.width,res.height, sl.MAT_TYPE.U8_C4)
    #while viewer.is_available():
    for i in range(100):
        if zed.grab() == sl.ERROR_CODE.SUCCESS :
        # Retrieve the left image in sl.Mat
            zed.retrieve_image(image_zed, sl.VIEW.DEPTH)
            zed.retrieve_image(image, sl.VIEW.LEFT)
            # Use get_data() to get the numpy array
            image_ocv = image_zed.get_data()
            orig_img = image.get_data()
            print(image_ocv.shape)
            #outfile = TemporaryFile()
            #np.save(outfile, image_ocv)
            image_ocv = image_ocv.reshape(image_ocv.shape[0], -1)
            image_ocv = cv2.resize(image_ocv,(1280,420))
            orig_img = orig_img.reshape(orig_img.shape[0], -1)
            orig_img = cv2.resize(orig_img,(1280,420))
            # Start contour boxing
            # Set and apply threshold
            threshold = 60
            pit_count = 0
            threshold_mat = np.where(image_ocv < threshold, 0, 255)
            threshold_mat = np.uint8(threshold_mat)
            # Noise removal
            threshold_mat = cv2.medianBlur(threshold_mat,7)
            # Edge detection
            edges = cv2.Canny(threshold_mat,100,200)
            # Find contours
            contours, hierarchy=cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
            # Convert to BGR to display
            threshold_mat = cv2.cvtColor(threshold_mat, cv2.COLOR_GRAY2BGR) 
            for c in contours:
                x,y,w,h=cv2.boundingRect(c)
                if(w*h > 30000):
                  cv2.rectangle(threshold_mat,(x,y),(x+w,y+h),(0,0,255),2)
                  cv2.putText(threshold_mat, 'PIT '+str(pit_count)+ ' DETECTED', (x, y+h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                  pit_count+=1;
                  #break;
                  # cv2_imshow(threshold_mat)
            #np.savetxt('test3.txt', image_ocv, fmt='%d')
            cv2.namedWindow('Image',cv2.WINDOW_NORMAL)
            cv2.namedWindow('Original',cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Image',1000,400)
            cv2.resizeWindow('Original',1000,400)
            cv2.imshow("Image",orig_img)
            cv2.imshow("Original",image_ocv)
            cv2.waitKey(1000)
            pit_count = 0
    cv2.destroyAllWindows()
    # Display the left image from the numpy array
        
    #zed.close()
'''
        if zed.grab() == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA,sl.MEM.CPU, res)
            zed.retrieve_image(image, sl.VIEW.LEFT,sl.MEM.CPU, res) # Get the left image
            zed.retrieve_image(depth, sl.VIEW.DEPTH,sl.MEM.CPU, res) # Retrieve depth matrix. Depth is aligned on the left RGB image
            depth_image_ocv = depth.get_data()
            cv2.imshow("Depth", depth_image_ocv)
            print(depth_image_ocv)
            viewer.updateData(image)
    '''
    #viewer.exit()

'''
    import matplotlib.pyplot as plt
    new = depth.get_data()
    plt.imshow(new)
    for i in range(res.height):
        for j in range(res.width):
            err,new[i][j] = depth.get_value(i,j)
'''



