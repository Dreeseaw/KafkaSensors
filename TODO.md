# Todo
- general
- api
  - turn into flask image, make simple route
    - given {sensor_id, trav_type, start_time, end_time},
      return [{window_time, trav_type, min, max, count, total_speed}]
      for all windows in given time frame
- display
  - get a simple query form working
  - get a react-vis chart for both metric types given the data
    - need to 0 pad for excluded periods of time
    - need to combine the 3 trav types for "all types" queries
  - start with only single-sensor queries, do multi if I have time
  - real-time updates?
