-- curLat 当前纬度
-- curLon 当前经度
-- shopLat 店铺纬度
-- shopLon 店铺经度


CREATE FUNCTION getDistance(curLat DOUBLE, curLon DOUBLE, shopLat DOUBLE, shopLon DOUBLE)
RETURNS DOUBLE
BEGIN
  DECLARE  dis DOUBLE;
    set dis = ACOS(SIN((curLat * 3.1415) / 180 ) * SIN((shopLat * 3.1415) / 180 ) + COS((curLat * 3.1415) / 180 ) * COS((shopLat * 3.1415) / 180 ) * COS((curLon * 3.1415) / 180 - (shopLon * 3.1415) / 180 ) ) * 6380 ;
    RETURN dis;
END;


