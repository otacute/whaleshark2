# whaleshark
LS 빅데이터 스쿨 2번째 팀 프로젝트 고래상어조

우리만의 Q칙!
1. 자기 파일만 건들어서 수정한다.
2. 커밋시간을 만들어 순차대로 커밋한다.
3. 조장만 통합본 파이를 건들수 있다.
4. 자기가 커밋하기전에 혹시 모르니까 풀땡기고 푸시하기


**df이름**
하우스정보 및 위도 경도 있는 df       : house
house 위도 경도만 가져온 df           : house_loc
핫스팟정보 및 위도 경도 있는 df       : hot_spot
hot_spot 위도 경도만 가져온 df        : spot_loc
hot_spot의 이미지 링크를 추가한거 df  : hot_sopt_add
hot_spot의 카테고리별 df              : spot_'카테고리' (총 3개)      ex) spot_Cultural



**주의사항**
1. house_loc과 spot_loc 위도, 경도 순서 다름
   - house_loc은 열 순서가 Longitude   Latitude
   - spot_loc은 열 순서가  Latitude  Longitude

2. house 1열 이름이 Unnamed: 0여서 Id로 고쳐야 합니다.