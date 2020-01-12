import csv
import cv2
import glob
def parse_epic_dataset(filename):
    action_list=[]
    uid_list=[]
    interested_actions = ['0']
    selected_videos=['P01_01']
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            uid = row['uid']
            actions = row['verb_class']
            video_id= row['video_id']
            if video_id in selected_videos:
                if actions in interested_actions:
                    #snipppet for actions
                    #read 1 frame in 6 frames to get 5frames per seconds
                    start_frame=row['start_frame']
                    stop_frame=row['stop_frame']
                    uid_list.append(uid)
                    action_list.append({'class':actions,'start':start_frame,'end':stop_frame})
    return {'video_id':video_id,'uid': uid_list, 'action_list': action_list}


if __name__ == '__main__':
    # need to add argparse

    info=parse_epic_dataset('EPIC_train_action_labels.csv')
    root='/media/chinmaya/eb18085f-17e0-4c19-8159-c2ae3d6b2325/Epic_data/EPIC_KITCHENS_2018/frames_rgb_flow/rgb/train/P01/P01_01/'
    path = root + '*.jpg'
    img_array = []
    for filename in sorted(glob.glob(path)):
        splitfilename = filename.split('frame_')[1]
        current = int(filename.split('frame_')[1].split('.')[0])

        # print(filename)
        img = cv2.imread(filename)

        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)
    for i in range(len(info['uid'])):
        #print(info['uid'][i])
        start=int(info['action_list'][i]['start'])-10
        stop=int(info['action_list'][i]['end'])


        key=0
        count = 0






        for filename in sorted(glob.glob(path)):
            splitfilename=filename.split('frame_')[1]
            current=int(filename.split('frame_')[1].split('.')[0])

            if current > start and current <stop:
                #print(filename)
                img = cv2.imread(filename)
                if count%10==0:
                    froot='/media/chinmaya/eb18085f-17e0-4c19-8159-c2ae3d6b2325/Epic_data/annotation/'
                    vroot='/media/chinmaya/eb18085f-17e0-4c19-8159-c2ae3d6b2325/Epic_data/annotation_video/'
                    full_path=froot+info['uid'][i]+'_'+splitfilename
                    #cv2.imwrite(full_path, img)
                    append='https://epic-kitchens-dataset.s3.amazonaws.com/'
                    #print(append+info['uid'][i]+'_'+splitfilename)
                    video_name = vroot+info['uid'][i] +'_'+splitfilename.split('.')[0] +'.mp4'
                    print(append + info['uid'][i] + '_' + splitfilename.split('.')[0] +'.mp4')

                    out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'MP4V'), 15, size)
                    for m in range(count,count+50):
                        out.write(img_array[m])
                    out.release()

            count=count+1