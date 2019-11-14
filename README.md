## bike_crawler
따릉이 대여소 정보 크롤러, 따릉이 대여소 현황

### 하기 링크의 서울시 따릉이 정보를 크롤링하여 csv, 엑셀으로 저장.


https://www.bikeseoul.com/app/station/moveStationSearchView.do?currentPageNo=1

[CLI version] : 1 페이지 ~ 특정 페이지 내용을 CSV로 저장.

[GUI version] : 시작 페이지 ~ 종료페이지 내용을 xlsx로 저장 or postgresql DB에 "Bike" 테이블로 저장.


<img src="bike_crawler/gui_version.png">

### [bike excel 2개 버전 비교]
<img src="bike_crawler/compare_excel.png">

### index 설명
    new : 새로생긴 row
    del : 삭제된 row
    U : 명칭변경
    X : X좌표변경
    Y : Y좌표변경.