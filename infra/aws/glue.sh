#!/bin/sh

DATABASE=$1

aws glue update-table --database-name "${DATABASE}" --table-input '{
    "Name":"usage_information_partitioned",
    "StorageDescriptor":{
        "Columns":[
            {
                "Name":"대여소번호",
                "Type":"int"
            },
            {
                "Name":"대여소",
                "Type":"string"
            },
            {
                "Name":"대여구분코드",
                "Type":"string"
            },
            {
                "Name":"성별",
                "Type":"string"
            },
            {
                "Name":"연령대코드",
                "Type":"string"
            },
            {
                "Name":"이용건수",
                "Type":"int"
            },
            {
                "Name":"운동량",
                "Type":"double"
            },
            {
                "Name":"탄소량",
                "Type":"double"
            },
            {
                "Name":"이동거리(m)",
                "Type":"double"
            },
            {
                "Name":"이용시간(분)",
                "Type":"int"
            }],
        "Location":"s3://public-bike/public_bike/usage_information/usage_information_partitioned",
				"InputFormat":"org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat",
				"OutputFormat":"org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat",
				"SerdeInfo": {
				    "SerializationLibrary":"org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe",
				    "Parameters":{
				        "compression":"gzip",
				        "path":"s3://public-bike/public_bike/usage_information/usage_information_partitioned",
				        "serialization.format":"1"
				    }
				}
		},
    "PartitionKeys": [{"Name":"대여일자", "Type":"string"}],
    "TableType": "MANAGED_TABLE",
    "Parameters":{
        "spark.sql.sources.schema.numPartCols":"1",
        "spark.sql.sources.schema.partCol.0":"MANAGED_TABLE",
        "spark.sql.partitionProvider":"catalog",
        "spark.sql.sources.schema.numParts":"1",
        "spark.sql.sources.provider":"parquet",
        "spark.sql.sources.schema.part.0": "{\"type\":\"struct\",\"fields\":[{\"name\":\"대여소번호\",\"type\":\"int\",\"nullable\":true,\"metadata\":{}},{\"name\":\"대여소\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"대여구분코드\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"성별\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"연령대코드\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}},{\"name\":\"이용건수\",\"type\":\"int\",\"nullable\":true,\"metadata\":{}},{\"name\":\"운동량\",\"type\":\"double\",\"nullable\":true,\"metadata\":{}},{\"name\":\"탄소량\",\"type\":\"long\",\"double\":true,\"metadata\":{}},{\"name\":\"이동거리(m)\",\"type\":\"double\",\"nullable\":true,\"metadata\":{}},{\"name\":\"이용시간(분)\",\"type\":\"int\",\"nullable\":true,\"metadata\":{}},{\"name\":\"대여일자\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}}]}",
        "spark.sql.create.version":"3.1.2-amzn-1"
    }
}'
