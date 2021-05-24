import numpy as np
import cv2

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink max-buffers=1 drop=true"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def process(frame):
    rect_size = 100
    h_sensivity = 20
    s_h = 255
    v_h = 255
    s_l = 50
    v_l = 50
    width, height, channels = frame.shape
    start_point = (int(width/2 - rect_size/2), int(width/2 - rect_size/2))
    end_point = (int(width/2 + rect_size/2), int(width/2 + rect_size/2))
    color = (255, 0, 0)
    thickness = 2
    rect = cv2.rectangle(frame, start_point, end_point, color, thickness)
    
    start_point_2 = (int(width/4 - rect_size/2), int(width/2 - rect_size/2))
    end_point_2 = (int(width/4 + rect_size/2), int(width/2 + rect_size/2))
    color_2 = (0,255,0)
    rect_2 = cv2.rectangle(frame, start_point_2, end_point_2, color_2, thickness)
    
    start_point_3 = (int(width*3/4 - rect_size/2), int(width/2 - rect_size/2))
    end_point_3 = (int(width*3/4 + rect_size/2), int(width/2 + rect_size/2))
    color_3 = (0,0,255)
    rect_3 = cv2.rectangle(frame, start_point_3, end_point_3, color_3, thickness)
    
    start_point_4 = (int(width - rect_size/2), int(width/2 - rect_size/2))
    end_point_4 = (int(width + rect_size/2), int(width/2 + rect_size/2))
    color_4 = (127,127,127)
    rect_4 = cv2.rectangle(frame, start_point_4, end_point_4, color_4, thickness)
    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    green_upper = np.array([60 + h_sensivity, s_h, v_h])
    green_lower = np.array([60 - h_sensivity, s_l, v_l])
    mask_frame = hsv_frame[start_point[1]:end_point[1] + 1, start_point[0]:end_point[0] + 1]
    mask_green = cv2.inRange(mask_frame, green_lower, green_upper)

    green_rate = np.count_nonzero(mask_green)/(rect_size*rect_size)

    #org = end_point
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.7
    size = cv2.getTextSize(text = ' green ', fontFace = font, fontScale = fontScale, thickness = thickness)
    org = (start_point[0], end_point[1]+size[0][1])
	
    if green_rate > 0.9:
        text = cv2.putText(rect, ' green ', org, font, fontScale, color, thickness, cv2.LINE_AA)
    else:
        text = cv2.putText(rect, ' not green ', org, font, fontScale, color, thickness, cv2.LINE_AA)
    
    hsv_frame_1 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blue_upper = np.array([110 + h_sensivity, s_h, v_h])
    blue_lower = np.array([110 - h_sensivity, s_l, v_l])
    mask_frame_1 = hsv_frame[start_point_2[1]:end_point_2[1] + 1, start_point_2[0]:end_point_2[0] + 1]
    mask_blue = cv2.inRange(mask_frame_1, blue_lower, blue_upper)

    blue_rate = np.count_nonzero(mask_blue)/(rect_size*rect_size)

    size_1 = cv2.getTextSize(text = ' blue ', fontFace = font, fontScale = fontScale, thickness = thickness)
    org_1 = (start_point_2[0], end_point_2[1]+size_1[0][1])
	
    if blue_rate > 0.9:
        text = cv2.putText(rect, ' blue ', org_1, font, fontScale, color_2, thickness, cv2.LINE_AA)
    else:
        text = cv2.putText(rect, ' not blue ', org_1, font, fontScale, color_2, thickness, cv2.LINE_AA)
        
    hsv_frame_2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray_upper = np.array([180, s_l, 127+h_sensivity*3])
    gray_lower = np.array([0, 0, 127-h_sensivity*3])
    mask_frame_2 = hsv_frame[start_point_3[1]:end_point_3[1] + 1, start_point_3[0]:end_point_3[0] + 1]
    mask_gray = cv2.inRange(mask_frame_2, gray_lower, gray_upper)

    gray_rate = np.count_nonzero(mask_gray)/(rect_size*rect_size)

    size_2 = cv2.getTextSize(text = ' gray ', fontFace = font, fontScale = fontScale, thickness = thickness)
    org_2 = (start_point_3[0], end_point_3[1]+size_2[0][1])
	
    if gray_rate > 0.9:
        text = cv2.putText(rect, ' gray ', org_2, font, fontScale, color_3, thickness, cv2.LINE_AA)
    else:
        text = cv2.putText(rect, ' not gray ', org_2, font, fontScale, color_3, thickness, cv2.LINE_AA)
        
    hsv_frame_3 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red_upper = np.array([0+h_sensivity, s_h, v_h])
    red_lower = np.array([0-h_sensivity, s_l, v_l])
    mask_frame_3 = hsv_frame[start_point_4[1]:end_point_4[1] + 1, start_point_4[0]:end_point_4[0] + 1]
    mask_red = cv2.inRange(mask_frame_3, red_lower, red_upper)
    
    hsv_frame_4 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red_upper_1 = np.array([180+h_sensivity, s_h, v_h])
    red_lower_1 = np.array([180-h_sensivity, s_l, v_l])
    mask_frame_4 = hsv_frame[start_point_4[1]:end_point_4[1] + 1, start_point_4[0]:end_point_4[0] + 1]
    mask_red_1 = cv2.inRange(mask_frame_4, red_lower, red_upper)
    
    red_rate = max(np.count_nonzero(mask_red)/(rect_size*rect_size),np.count_nonzero(mask_red_1)/(rect_size*rect_size))

    size_3 = cv2.getTextSize(text = ' red ', fontFace = font, fontScale = fontScale, thickness = thickness)
    org_3 = (start_point_4[0], end_point_4[1]+size_3[0][1])
	
    if red_rate > 0.9:
        text = cv2.putText(rect, ' red ', org_3, font, fontScale, color_4, thickness, cv2.LINE_AA)
    else:
        text = cv2.putText(rect, ' not red ', org_3, font, fontScale, color_4, thickness, cv2.LINE_AA)

    av_hue = np.average(mask_frame_2[:,:,0])
    av_sat = np.average(mask_frame_2[:,:,1])
    av_val = np.average(mask_frame_2[:,:,2])
    average = [int(av_hue),int(av_sat),int(av_val)]
    
    text = cv2.putText(rect, str(average) + " " + str(gray_rate), (10,50), font, fontScale, color, thickness, cv2.LINE_AA)
    frame = text
    return frame

print('Press 4 to Quit the Application\n')

#Open Default Camera
cap = cv2.VideoCapture(0)#gstreamer_pipeline(flip_method=4), cv2.CAP_GSTREAMER)

while(cap.isOpened()):
    #Take each Frame
    ret, frame = cap.read()
    
    #Flip Video vertically (180 Degrees)
    frame = cv2.flip(frame, 180)

    invert = process(frame)

    # Show video
    cv2.imshow('Cam', frame)

    # Exit if "4" is pressed
    k = cv2.waitKey(1) & 0xFF
    if k == 52 : #ord 4
        #Quit
        print ('Good Bye!')
        break

#Release the Cap and Video   
cap.release()
cv2.destroyAllWindows()
