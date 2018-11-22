#!/usr/bin/env python
"""
2018/11/22 moriitkys
If color and depth image topics  are received, 
you can get depth value by using this program.
This program is an example of getting the depth at the center of the image.
This program is for topics from RealSense D415/435, 
but you can use other devices by changing topic name.
"""
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class ColorDepthEdit(object):
    def __init__(self):
        self._image_pub = rospy.Publisher('image', Image, queue_size=1)
        self._depth_pub = rospy.Publisher('depth_image', Image, queue_size=1)
        self._image_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.image_callback, queue_size=1)
        self._depth_sub = rospy.Subscriber('/camera/depth/image_rect_raw', Image, self.depth_callback, queue_size=1)
        self._bridge = CvBridge()
        self.m_depth = 0.0

    def image_callback(self, data):
        try:
            cv_image = self._bridge.imgmsg_to_cv2(data, 'bgr8')
        except CvBridgeError, e:
            print e

        try:
            img_out = self.img_processing(self.img_edit(cv_image))
            self._image_pub.publish(self._bridge.cv2_to_imgmsg(img_out, 'bgr8'))
        except CvBridgeError, e:
            print e

    def depth_callback(self, data):
        try:
            self._depth_pub.publish(data)
            cv_dimage = self._bridge.imgmsg_to_cv2(data, 'passthrough')
        except CvBridgeError, e:
            print e
        h, w = cv_dimage.shape[:2]
        #you should change under 2 lines if you don't use realsense
        depth_array = np.array(cv_dimage, dtype=np.float32)
        depth_img = depth_array * 255/65535
        depth_img2 = np.array(depth_img, dtype=np.uint8)
        depth_color_img = np.stack((depth_img2,)*3, axis=-1)

        # Extract the center of depth image (20x20 pixels)
        depth_array2 = depth_array[h/2-10:h/2+10, w/2-10:w/2+10]
        depth_array3 = depth_array2[depth_array2 > 0]

        self.m_depth = np.mean(depth_array3)
        print('The mean depth value at the center of image is', self.m_depth)

        depth_out = self.img_edit(depth_color_img)

        try:
            self._depth_pub.publish(self._bridge.cv2_to_imgmsg(depth_out, 'bgr8'))
        except CvBridgeError, e:
            print e

    def img_edit(self, img):
        """
        show a character or figures on the image
        """
        h, w = img.shape[:2]
        cv2.rectangle(img, (w/2-10, h/2-10), (w/2+10, h/2+10), (0, 0, 255), 3)
        fontType = cv2.FONT_HERSHEY_SIMPLEX
        text = str(self.m_depth) + 'mm'
        cv2.putText(img, text, (w/2 +20, h/2 + 20), fontType, 1, (0, 0, 255),2)
        return img

    def img_processing(self, img):
        """
        This is the example of image processing
        apply gamma correction to color image
        """
        gamma = 2.5
        lookup_table = np.zeros((256, 1), dtype = 'uint8')
        for i in range(256):
	    lookup_table[i][0] = 255 * pow(float(i) / 255, 1.0 / gamma)
        img_src = img
        img_gamma = cv2.LUT(img_src, lookup_table)
        return img_gamma

if __name__ == '__main__':
    rospy.init_node('ColorDepthEdit')
    image_depth_pub = ColorDepthEdit()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        pass

