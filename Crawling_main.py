import numpy
import pandas
from scipy import io
import os
import subprocess
import pytube
import sys


mat_file =io.loadmat('golfDB.mat')  # mat file 불러오기
data = mat_file['golfDB']           # raw_data[0][0~1399]
Ndata = len(data[0])                # 전체 갯수


mp4dir = 'video'
if not os.path.isdir(mp4dir):
	os.mkdir(mp4dir)

fname = os.path.join(mp4dir,'[Down_History].txt')
f_save = open(fname, 'w')
str_header = 'Num\tID\tYoutube_id\tVideo Name\n'
f_save.write(str_header)

cnt = 0
prev_id = ''
for idx in range(0, Ndata):
    # print(data[0][idx])
    id = data[0][idx][0][0][0]  # data parsing
    youtube_id = data[0][idx][1][0]
    slow =  data[0][idx][6][0]
    events = data[0][idx][7][0]
    bbox = data[0][idx][8][0]

    if youtube_id != prev_id:  # 중복 데이터 제거
        cnt += 1
        print(cnt, id, youtube_id)
        url = 'https://www.youtube.com/watch?v=' + youtube_id   # Youtube URL
        yt = pytube.YouTube(url)  # 다운받을 동영상 URL 지정
        vids = yt.streams.first().download(mp4dir)  # 가장 첫 번째 스트림(가장 고화질)
        # vids = yt.streams.all()
        # for i in range(len(vids)):  # 영상 형식 리스트 확인
        #     print(i, '. ', vids[i])

        vids = vids.split("/")
        str_note = str(cnt) + '\t' + str(id) + '\t' + str(youtube_id) + '\t' + str(vids[1]) + '\n'
        f_save.write(str_note)  # log 저장

    prev_id = youtube_id


f_save.close()
print('Download Complete')



