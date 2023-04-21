import os
import sys
import glob
import datetime
from datetime import datetime
import pandas as pd

from models.store import Store
from models.brand import Brand

from modules.query_processor import Query_Processor

from shopifycode.shopify_updater import Shopify_Updater

class Controller:
    def __init__(self, DEBUG: bool, path: str) -> None:
        self.DEBUG = DEBUG
        self.store: Store = None
        self.path: str = path
        self.config_file: str = f'{self.path}/files/config.json'
        self.logs_folder_path: str = ''
        self.logs_filename: str = ''
        pass

    def update_inventory_controller(self) -> None:
        try:
            
            # getting all stores from database
            query_processor = Query_Processor(self.DEBUG, self.config_file, '')
            stores = query_processor.get_stores()

            for store in self.get_store_to_update(stores):
                self.store = store
                query_processor.database_name = str(self.store.name).lower()
                self.logs_folder_path = f'{self.path}/Logs/{self.store.name}/'
                
                if not os.path.exists('Logs'): os.makedirs('Logs')
                if not os.path.exists(self.logs_folder_path): os.makedirs(self.logs_folder_path)
                self.create_logs_filename()
                self.remove_extra_log_files()

                # getting all brands of store from database
                self.store.brands = query_processor.get_brands()
                if self.store.brands:
                    shopify_obj = Shopify_Updater(self.DEBUG, self.store, self.config_file, query_processor, self.logs_filename)
                    shopify_obj.update_inventory_controller()
                    self.create_excel_file(shopify_obj)
                else: print('No brand selected to scrape and update') 
        except Exception as e:
            if self.DEBUG: print(f'Exception in update_inventory_controller: {e}')
            else: pass

    def update_product_controller(self, field_to_update: str) -> None:
        try:
            # getting all stores from database
            query_processor = Query_Processor(self.DEBUG, self.config_file, '')
            stores = query_processor.get_stores()

            for store in self.get_store_to_update(stores):
                self.store = store
                query_processor.database_name = str(self.store.name).lower()
                self.logs_folder_path = f'{self.path}/Logs/{self.store.name}/'
                
                if not os.path.exists('Logs'): os.makedirs('Logs')
                if not os.path.exists(self.logs_folder_path): os.makedirs(self.logs_folder_path)
                self.create_logs_filename()
                self.remove_extra_log_files()

                # getting all brands of store from database
                all_brands = query_processor.get_brands()

                # getting user selected brands to scrape and update
                self.store.brands = self.get_brands_to_update(all_brands)

                if self.store.brands:
                    for brand in self.store.brands:
                        # getting user selected product type for each brand 
                        selected_product_types = self.get_product_type_to_update(brand, brand.product_types)
                        if selected_product_types: brand.product_types = selected_product_types
                        else: print(f'No product type selected for {brand.name}')
                                
                    if field_to_update in ['Update Product Title and Description', 'Update Product Images', 'Update Product Tags']:
                        Shopify_Updater(self.DEBUG, self.store, self.config_file, query_processor, self.logs_filename).update_product(field_to_update)
                    elif field_to_update == 'Update Metafields':
                        Shopify_Updater(self.DEBUG, self.store, self.config_file, query_processor, self.logs_filename).update_product_metafields()
                        
                else: print('No brand selected to scrape and update') 
        except Exception as e:
            if self.DEBUG: print(f'Exception in update_product_controller: {e}')
            else: pass

    # create logs filename
    def create_logs_filename(self) -> None:
        try:
            scrape_time = datetime.now().strftime('%d-%m-%Y %H-%M-%S')
            self.logs_filename = f'{self.logs_folder_path}Logs {scrape_time}.txt'
        except Exception as e:
            self.print_logs(f'Exception in create_logs_filename: {str(e)}')
            if self.DEBUG: print(f'Exception in create_logs_filename: {e}')
            else: pass

    # print logs to the log file
    def print_logs(self, log: str):
        try:
            with open(self.logs_filename, 'a') as f:
                f.write(f'\n{log}')
        except: pass

    def get_store_to_update(self, stores: list[Store]) -> list[Store]:
        selected_stores = []
        try:
            print('\nSelect any store to update:')
            for store_index, store in enumerate(stores):
                print(store_index + 1, store.name)

            while True:
                store_choices = 0
                try:
                    store_choices = input('Choice: ')
                    if store_choices:
                        for store_choice in store_choices.split(','):
                            selected_stores.append(stores[int(store_choice) - 1])
                        break
                    else: print(f'Please enter number from 1 to {len(stores)}')
                except: print(f'Please enter number from 1 to {len(stores)}')
        except Exception as e:
            if self.DEBUG: print(f'Exception in get_store_to_update: {e}')
            else: pass
        finally: return selected_stores

    def get_brands_to_update(self, brands: list[Brand]) -> list[Brand]:
        selected_brands = []
        try:
            print('\nSelect brands to scrape and update:')
            for brand_index, brand in enumerate(brands):
                print(brand_index + 1, brand.name)


            while True:
                brand_choices = ''
                try:
                    brand_choices = input('Choice: ')
                    if brand_choices:
                        for brand_choice in brand_choices.split(','):
                            selected_brands.append(brands[int(str(brand_choice).strip()) - 1])
                        break
                    else: print(f'Please enter number from 1 to {len(brands)}')
                except Exception as e:
                    print(f'Please enter number from 1 to {len(brands)}')
        except Exception as e:
            if self.DEBUG: print(f'Exception in get_brands_to_update: {e}')
            else: pass
        finally: return selected_brands
    
    # get brands product types of user choice
    def get_product_type_to_update(self, brand: Brand, product_types: list[str]) -> list[str]:
        selected_product_types = []
        try:
            print(f'\nSelect product type to update for {brand.name}:')
            for product_type_index, product_type in enumerate(product_types):
                print(product_type_index + 1, str(product_type).title())


            while True:
                product_type_choices = ''
                try:
                    product_type_choices = input('Choice: ')
                    if product_type_choices:
                        for product_type_choice in product_type_choices.split(','):
                            selected_product_types.append(product_types[int(str(product_type_choice).strip()) - 1])
                        break
                    else: 
                        selected_product_types = []
                        print(f'Product type cannot be empty')
                except Exception as e:
                    if self.DEBUG: print(e) 
                    selected_product_types = []
                    print(f'Please enter number from 1 to {len(product_types)}')

        except Exception as e:
            if self.DEBUG: print(f'Exception in get_product_type_to_update: {e}')
            else: pass
        finally: return selected_product_types

    # create excel file of results
    def create_excel_file(self, shopify_obj: Shopify_Updater):
        try:
            data = []
            path = ''
            filename = f'{path}{self.store.name} {datetime.now().strftime("%d-%m-%Y")} Results.xlsx'

            data.append( 
                (
                    'Brands and types', {
                    "Brand": [brand.name for brand in self.store.brands], 
                    "Types": [', '.join(brand.product_types) for brand in self.store.brands]
                    } 
                ) 
            )
            if shopify_obj.new_products:
                new_products_tuple = (
                    'New Products', {
                        'Title' : [sublist[0] for sublist in shopify_obj.new_products], 
                        'Vendor' : [sublist[1] for sublist in shopify_obj.new_products], 
                        'Product Type' : [sublist[2] for sublist in shopify_obj.new_products], 
                        'Variant SKU' : [sublist[3] for sublist in shopify_obj.new_products], 
                        'Price' : [sublist[4] for sublist in shopify_obj.new_products], 
                        'Inventory Quantity' : [sublist[5] for sublist in shopify_obj.new_products]
                    }
                )
                data.append(new_products_tuple)
            if shopify_obj.new_variants:
                new_variants_tuple = (
                    'New Variants', {
                        'Vendor' : [sublist[0] for sublist in shopify_obj.new_variants], 
                        'Product Type' : [sublist[1] for sublist in shopify_obj.new_variants], 
                        'Variant SKU' : [sublist[2] for sublist in shopify_obj.new_variants], 
                        'Price' : [sublist[3] for sublist in shopify_obj.new_variants],
                        'Inventory Quantity' : [sublist[4] for sublist in shopify_obj.new_variants]
                    }
                )
                data.append(new_variants_tuple)
            if shopify_obj.updated_variants:
                found_variants_tuple = (
                    'Found Variants', {
                        'Vendor' : [sublist[0] for sublist in shopify_obj.updated_variants], 
                        'Product Type' : [sublist[1] for sublist in shopify_obj.updated_variants],
                        'Variant SKU' : [sublist[2] for sublist in shopify_obj.updated_variants],
                        'Price' : [sublist[3] for sublist in shopify_obj.updated_variants],
                        'Compare At Price' : [sublist[4] for sublist in shopify_obj.updated_variants],
                        'Inventory Quantity' : [sublist[5] for sublist in shopify_obj.updated_variants]
                    }
                )
                data.append(found_variants_tuple)
            if shopify_obj.not_found_variants:
                not_found_variants_tuple = (
                    'Not found Variants', {
                        'Vendor' : [sublist[0] for sublist in shopify_obj.not_found_variants], 
                        'Product Type' : [sublist[1] for sublist in shopify_obj.not_found_variants],
                        'Variant SKU' : [sublist[2] for sublist in shopify_obj.not_found_variants],
                        'Price' : [sublist[3] for sublist in shopify_obj.not_found_variants],
                        'Compare At Price' : [sublist[4] for sublist in shopify_obj.not_found_variants],
                        'Inventory Quantity' : [sublist[5] for sublist in shopify_obj.not_found_variants]
                    }
                )
                data.append(not_found_variants_tuple)

            if data:
                writer = pd.ExcelWriter(filename, engine='xlsxwriter')
                for sheet_name, sheet_data in data:
                    df = pd.DataFrame(sheet_data)
                    df.to_excel(writer, sheet_name=sheet_name, index=False)

                writer.close()
        except Exception as e:
            self.print_logs(f'Exception in create_excel: {str(e)}')
            if self.DEBUG: print(f'Exception in create_excel: {e}')
            else: pass

    # manage templates folder - create those folder and files which are needed and not created yet 
    def manage_template_folder(self, stores: list[Store], query_processor: Query_Processor) -> None:
        try:
            files = ['title.txt', 'product_description.txt', 'meta_title.txt', 'meta_description.txt', 'image_description.txt']
            
            if not os.path.exists('templates'): os.makedirs('templates')

            for store in stores:
            
                STORE_FOLDER_PATH = F'templates/{str(store.name).strip().title()}'
                if not os.path.exists(STORE_FOLDER_PATH): os.makedirs(STORE_FOLDER_PATH)

                # getting all brands of store from database
                brands = query_processor.get_brands_by_store_id(store.id)

                for brand in brands:
                    
                    BRAND_FOLDER_PATH = f'{STORE_FOLDER_PATH}/{str(brand.name).strip().title()}'
                    if not os.path.exists(BRAND_FOLDER_PATH): os.makedirs(BRAND_FOLDER_PATH)
                    
                    # getting all type of products for store
                    product_types = query_processor.get_product_types_by_store_id(store.id)

                    for product_type in product_types:

                        PRODUCT_TYPE_FOLDER_PATH = f'{BRAND_FOLDER_PATH}/{str(product_type).strip().title()}'
                        if not os.path.exists(PRODUCT_TYPE_FOLDER_PATH): os.makedirs(PRODUCT_TYPE_FOLDER_PATH)

                        for file in files:
                            FILE_PATH = f'{PRODUCT_TYPE_FOLDER_PATH}/{file}'
                            if not os.path.exists(FILE_PATH):
                                f = open(FILE_PATH, "x")
                                f.close()


        except Exception as e:
            self.print_logs(f'Exception in manage_template_folder: {e}')
            if self.DEBUG: print(f'Exception in manage_template_folder: {e}')

    # remove extra log files and keep latest 6 files 
    def remove_extra_log_files(self) -> None:
        try:
            files = glob.glob(f'{self.logs_folder_path}*.txt')
            while len(files) > 4:
                oldest_file = min(files, key=os.path.getctime)
                os.remove(oldest_file)
                files = glob.glob(f'{self.logs_folder_path}*.txt')
        except Exception as e:
            self.print_logs(f'Exception in remove_extra_log_files: {str(e)}')
            if self.DEBUG: print(f'Exception in remove_extra_log_files: {e}')
            else: pass

def get_field_to_update(DEBUG: bool):
    update_field = ''
    try:
        fields = ['Update Product Inventory', 'Update Product Title and Description', 'Update Product Images', 'Update Product Tags', 'Update Metafields']
        print('Select fields to update:')
        for field_index, field in enumerate(fields):
            print(f'{field_index + 1}. {field}')

        while True:
            field_choice = 0
            try:
                field_choice = int(input('Choice: '))
                if field_choice > 0 and field_choice <= len(fields):
                    update_field = fields[int(field_choice) - 1]
                    break
                else: print(f'Please enter number from 1 to {len(fields)}')
            except: print(f'Please enter number from 1 to {len(fields)}')
    except Exception as e:
        if DEBUG: print(f'Exception in get_update_fields: {e}')
    finally: return update_field

DEBUG = True
try:
    pathofpyfolder = os.path.realpath(sys.argv[0])
    # get path of Exe folder
    path = pathofpyfolder.replace(pathofpyfolder.split('\\')[-1], '')
    
    if '.exe' in pathofpyfolder.split('\\')[-1]: DEBUG = False

    field_to_update = get_field_to_update(DEBUG)
    if field_to_update:
        obj = Controller(DEBUG, path)
        if field_to_update == 'Update Product Inventory': obj.update_inventory_controller()
        else: obj.update_product_controller(field_to_update)

except Exception as e:
    if DEBUG: print('Exception: '+str(e))
    else: pass