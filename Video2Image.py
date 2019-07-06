import cv2
import sys
import os
from scipy import io


mat_file =io.loadmat('golfDB.mat')  # mat 파일 불러오기
matdata = mat_file['golfDB']        # raw_data[0][0~1399]
Ndata = len(matdata[0])             # 전체 행 갯수


video_folder = 'video'                                          # Youtube 영상 저장 폴더명
list_path = os.path.join(video_folder,'[Down_History].txt')     # Youtube 영상 다운로드 내역 경로
flist = open(list_path,'r')                                     # txt 파일 읽기
flist.readline()                                                # 헤더문자 건너띄기


flog = open(os.path.join(video_folder, '[Video2Image_Log].txt'), 'w')   # Image 저장 내역 txt 파일로 저장
flog.write('ID\tYoutube_ID\tslow\tFrame\tFolder Name\n')                # txt 파일 헤더



for raw in flist:  # mat 파일에서 line 별로 읽음
    data = raw.split('\t')
    id = int(data[1])
    video_id = data[2].split('\n')[0]
    video_name = data[3].split('\n')[0]
    print(data[0],'\t',id,'\t',video_id,'\t',video_name)

    for idx in range(int(data[1]), Ndata):  # 다운받은 영상 내역 읽음
        # print(matdata[0][idx])
        youtube_id = matdata[0][idx][1][0]
        slow = matdata[0][idx][6][0][0]
        events = matdata[0][idx][7][0]
        frame_start = events[0]; frame_end = events[len(events)-1]

        if youtube_id == video_id:  # mat 파일과 다운로드 내역 비교
            cam = cv2.VideoCapture(os.path.join(video_folder, video_name))
            currentframe = 1
            ii = 0
            while (True):
                ret, frame = cam.read()
                if (ret) and (ii >= frame_start) and (ii <= frame_end):  # Event 시작점 ~ Event 마지막 사이 저장

                    img_name = str(currentframe).zfill(4) + '.jpg'  # 저장 파일명
                    if slow:    # 저장 폴더명
                        video_name2 = str(id).zfill(4) + '_' + video_name.split('.mp4')[0] + '_slow'
                    else:
                        video_name2 = str(id).zfill(4) + '_' + video_name.split('.mp4')[0]
                    img_path = os.path.join(video_folder, video_name2, img_name)    # 이미지 저장경로
                    if not os.path.isdir(os.path.join(video_folder, video_name2)):  # 초기 한번만 폴더 생성
                        os.mkdir(os.path.join(video_folder, video_name2))

                    if (ii%5==0):    # n장 마다 이미지 저장
                        cv2.imwrite(img_path, frame)
                        currentframe += 1
                    ii += 1
                else:
                    ii += 1     # start frame까지 ii 증가

                if ii > frame_end:  # Event 마지막 지점 지나면 종료
                    str_log = str(id) +'\t'+ str(youtube_id) +'\t'+ str(slow) +'\t'+ str(currentframe-1) +'\t'+ video_name2
                    flog.write(str_log); flog.write('\n')   # 저장 log 저장
                    print("\t>> ", str_log)
                    break

        # elif youtube_id != video_id:
        #     break

        id+=1


flist.close()
cam.release()
cv2.destroyAllWindows()
