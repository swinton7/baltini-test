### Installation command
0. Install docker for mysql - you can google how to
0. Install Dbeaver for easier data analysis
0. Download Baltini dataset
1. `sudo docker run -d -p 3306:3306 -v ${PWD}/data:/var/lib/mysql --name mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=dummy_baltini mysql:latest`
2. `sudo docker exec -i mysql sh -c 'exec mysql -uroot -proot -D dummy_baltini' < 127-0-0-1dummy_baltini20231206-12-23.sql`
3. For daily, just put the code inside cron job or any orchestrator, code can already accept daily
4. run `python create_merger_list.py` to create files to be loaded
5. run `python load_data.py` to load the generated data
6. Use the `result_query.sql` to generate result

I temporarily used this date `2023-10-16` for reproducibility

python=3.12

### DATABASE
dummy_baltini

### TABLES
- brands
- product_duplicate_lists
- product_duplicates
- product_images
- product_options
- product_variant_options
- product_variants
- products <- we use this
- retailers
- seasons
- suppliers
