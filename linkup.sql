UPDATE linkupapi_match
SET date = "2023-05-18"
WHERE date = "2023-06-18"

UPDATE linkupapi_golfermatch
SET golfer_id = 4
WHERE golfer_id = 1

DELETE from linkupapi_message
Where id > 6

DELETE from linkupapi_holescore
Where id > 87