# Populating the database

## Run 1
`python project-2.py --files Baselight_JJacobs_20230323.txt Flame_DFlowers_20230323.txt Flame_MFelix_20230323.txt --verbose --xytech Xytech_20230323.txt --output db`

## Run 2
`python project-2.py --files Baselight_TDanza_20230324.txt --verbose --xytech Xytech_20230324.txt --output db`

## Run 3
`python project-2.py --files Baselight_GLopez_20230325.txt --verbose --xytech Xytech_20230325.txt --output db`

## Run 4
`python project-2.py --files Baselight_BBonds_20230326.txt Flame_DFlowers_20230326.txt --verbose  --xytech Xytech_20230326.txt -–output db`

## Run 5
`python project-2.py --files Baselight_THolland_20230327.txt Flame_BBonds_20230327.txt --verbose  --xytech Xytech_20230327.txt --output db`

# Querying the database
## 1. List all work done by user BBonds
In jobs collection: `{user_on_file: "BBonds"}`
## 2. All work done after 3-25-2023 date on a Flame
In files collection: `{machine: 'Flame',date_of_file: {$gt: '20230325'}}`

jobs: `{$or: [{user_on_file: "BBonds", date_of_file: "20230327"}, {user_on_file: "DFlowers", date_of_file: "20230326"}]}`
## 3. What work done on ddnsata7 on date 3-23-2023
In jobs: `{location: {$regex: "ddnsata7"}, date_of_file: "20230323"}`
## 4. Name of all Autodesk Flame users
```
db.getCollection('files').aggregate(
  [
    { $match: { machine: 'Flame' } },
    {
      $group: {
        _id: '$user_on_file',
        record: { $first: '$$ROOT' }
      }
    },
    { $replaceRoot: { newRoot: '$record' } }
  ],
  { maxTimeMS: 60000, allowDiskUse: true }
);
```
## 5. Name User(s) and Date(s) where they worked on hpsans15
In jobs: `{location: {$regex: "hpsans15"}}` (trick question; no data)