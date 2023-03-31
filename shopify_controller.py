import os
import sys
# import json
# import glob
import datetime
from datetime import datetime
import pandas as pd

from models.store import Store
from models.brand import Brand
from models.product import Product
# from models.metafields import Metafields
from models.variant import Variant

# from modules.files_reader import Files_Reader
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

    def controller(self) -> None:
        try:
            
            # getting all stores from database
            query_processor = Query_Processor(self.DEBUG, self.config_file, '')
            stores = query_processor.get_stores()

            self.store = self.get_store_to_update(stores)

            if self.store:
                query_processor.database_name = str(self.store.name).lower()
                self.logs_folder_path = f'{self.path}/Logs/{self.store.name}/'
                
                if not os.path.exists('Logs'): os.makedirs('Logs')
                if not os.path.exists(self.logs_folder_path): os.makedirs(self.logs_folder_path)
                if not self.logs_filename: self.create_logs_filename()

                # getting all brands of store from database
                all_brands = query_processor.get_brands()

                # getting user selected brands to scrape and update
                self.store.brands = self.get_brands_to_update(all_brands)

                if self.store.brands:
                    field_to_update = self.get_field_to_update()
                    if field_to_update:
                        for brand in self.store.brands:
                            brand.products = self.get_products(brand, query_processor)
                        
                        print('\n')

                        if field_to_update == 'Update Product Inventory':
                            shopify_obj = Shopify_Updater(self.DEBUG, self.store, self.config_file, query_processor, self.logs_filename)
                            shopify_obj.update_inventory_controller()
                            self.create_excel_file(shopify_obj)
                        elif field_to_update == 'Update Product Title and Description':
                            Shopify_Updater(self.DEBUG, self.store, self.config_file, query_processor, self.logs_filename).update_product_title_and_description()
                        elif field_to_update == 'Update Product Images':
                            Shopify_Updater(self.DEBUG, self.store, self.config_file, query_processor, self.logs_filename).update_product_images()
                        else:
                            print(field_to_update)
                else: print('No brand selected to scrape and update') 
        except Exception as e:
            if self.DEBUG: print(f'Exception in Shopify_Controller controller: {e}')
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

    def get_store_to_update(self, stores: list[Store]) -> Store:
        selected_store = None
        try:
            print('Select any store to update:')
            for store_index, store in enumerate(stores):
                print(store_index + 1, store.name)

            while True:
                store_choice = 0
                try:
                    store_choice = int(input('Choice: '))
                    if store_choice > 0 and store_choice <= len(stores):
                        selected_store = stores[int(store_choice) - 1]
                        break
                    else: print(f'Please enter number from 1 to {len(stores)}')
                except: print(f'Please enter number from 1 to {len(stores)}')
        except Exception as e:
            if self.DEBUG: print(f'Exception in get_store_to_update: {e}')
            else: pass
        finally: return selected_store

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

    def get_products(self, brand: Brand, query_processor: Query_Processor) -> list[Product]:
        products: list[Product] = []
        try:
            # for p_json in query_processor.get_products_by_brand(brand.name):
            for p_json in query_processor.get_all_product_details_by_brand_name(brand.name):
                product = Product()
                product.id = str(p_json['_id']).strip()
                product.number = str(p_json['number']).strip()
                product.name = str(p_json['name']).strip()
                product.brand = str(p_json['brand']).strip()
                product.frame_code = str(p_json['frame_code']).strip()
                product.lens_code = str(p_json['lens_code']).strip()
                product.type = str(p_json['type']).strip()
                product.bridge = str(p_json['bridge']).strip()
                product.template = str(p_json['template']).strip()
                product.shopify_id = str(p_json['shopify_id']).strip()
                product.metafields.for_who = str(p_json['metafields']['for_who']).strip()
                product.metafields.lens_material = str(p_json['metafields']['lens_material']).strip()
                product.metafields.lens_technology = str(p_json['metafields']['lens_technology']).strip()
                product.metafields.lens_color = str(p_json['metafields']['lens_color']).strip()
                product.metafields.frame_shape = str(p_json['metafields']['frame_shape']).strip()
                product.metafields.frame_material = str(p_json['metafields']['frame_material']).strip()
                product.metafields.frame_color = str(p_json['metafields']['frame_color']).strip()
                product.metafields.size_bridge_template = str(p_json['metafields']['size-bridge-template']).strip()
                product.metafields.gtin1 = str(p_json['metafields']['gtin1']).strip()
                product.image = str(p_json['image']).strip() if product.image else ''
                product.images_360 = p_json['images_360'] if p_json['images_360'] else []

                variants: list[variants] = []
                # for v_json in query_processor.get_variants_by_product_id(product.id):
                for v_json in p_json['variants']:
                    variant = Variant()
                    variant.id = str(v_json['_id']).strip()
                    variant.product_id = str(v_json['product_id']).strip()
                    variant.title = str(v_json['title']).strip() if 'title' in v_json else ''
                    variant.sku = str(v_json['sku']).strip()
                    variant.inventory_quantity = int(v_json['inventory_quantity'])
                    variant.found_status = int(v_json['found_status'])
                    variant.wholesale_price = float(v_json['wholesale_price'])
                    variant.listing_price = float(v_json['listing_price'])
                    variant.barcode_or_gtin = str(v_json['barcode_or_gtin']).strip()
                    variant.shopify_id = str(v_json['shopify_id']).strip()
                    variant.inventory_item_id = str(v_json['inventory_item_id']).strip()
                    variants.append(variant)

                product.variants = variants

                products.append(product)
        except Exception as e:
            if self.DEBUG: print(f'Exception in get_products: {e}')
            self.print_logs(f'Exception in get_products: {e}')
        finally: return products

    def get_field_to_update(self):
        update_field = ''
        try:
            fields = ['Update Product Inventory', 'Update Product Title and Description', 'Update Product Images', 'Update Product Tags', 'Update Metafields']
            print('\nSelect fields to update:')
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
            if self.DEBUG: print(f'Exception in get_update_fields: {e}')
            self.print_logs(f'Exception in get_update_fields: {str(e)}')
        finally: return update_field

    def create_excel_file(self, shopify_obj: Shopify_Updater):
        try:
            data = []
            path = ''
            try:
                choice = input('Save to sync? : ')
                if str(choice).strip().lower() in ['y', 'yes']: path = 'C:/Users/muham/Sync/Looker Online/Results/'
            except Exception as e: print(f'Exception in create_excel_file input: {e}')
            
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

DEBUG = True
try:
    pathofpyfolder = os.path.realpath(sys.argv[0])
    # get path of Exe folder
    path = pathofpyfolder.replace(pathofpyfolder.split('\\')[-1], '')
    
    if '.exe' in pathofpyfolder.split('\\')[-1]: DEBUG = False

    Controller(DEBUG, path).controller()

except Exception as e:
    if DEBUG: print('Exception: '+str(e))
    else: pass