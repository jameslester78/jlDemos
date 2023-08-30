CREATE VIEW parkrun_project1.firstRunAtEvent AS
SELECT event,min(rundate) AS rundate FROM completedRuns GROUP BY event
;
