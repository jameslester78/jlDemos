CREATE VIEW parkrun_project1.firstRunAtEvent AS
SELECT event,min(rundate) AS rundate FROM completedRuns GROUP BY event
;
CREATE VIEW parkrun_project1.allEvents
AS
SELECT    a.eventShortName,
          localAuthority,
          county,
          region,
          sss,
          travelTimeMins,
          travelDistanceKM,
          runDate
          
FROM      events a
LEFT JOIN firstRunAtEvent b ON a.eventShortName = b.event
LEFT JOIN sss c ON c.event = a.eventShortName
LEFT JOIN drivingDistances d ON d.eventShortName = a.eventShortName
LEFT JOIN regions e ON e.eventLongName = a.eventLongName