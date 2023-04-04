import os
import base64
import requests
from time import sleep
from PIL import Image

from models.store import Store
from models.brand import Brand
from models.product import Product

from modules.files_reader import Files_Reader

from shopifycode.shopify_processor import Shopify_Processor

class Utils:
    def __init__(self, DEBUG: bool, logs_filename: str) -> None:
        self.DEBUG: bool = DEBUG
        self.logs_filename: str = logs_filename
        pass

    def get_templates_folder_path(self, store_name: str) -> str:
        template_folder_path = ''
        try:
            if store_name == 'Digitalhub': template_folder_path = 'templates/Digitalhub/'
            elif store_name == 'Safilo': template_folder_path = 'templates/Safilo/'
            elif store_name == 'Keringeyewear': template_folder_path = 'templates/Keringeyewear/'
            elif store_name == 'Rudyproject': template_folder_path = 'templates/Rudyproject/'
            elif store_name == 'Luxottica': template_folder_path = 'templates/Luxottica/'
        except Exception as e:
            self.print_logs(f'Exception in get_templates_folder_path: {e}')
            if self.DEBUG: print(f'Exception in get_templates_folder_path: {e}')
            else: pass
        finally: return template_folder_path

    # get product template path 
    def get_template_path(self, field: str, brand: Brand, product: Product, template_file_path: str) -> str:
        template_path = ''
        try:
            if field == 'Product Title': template_path = f'{template_file_path}{brand.name}/{product.type}/title.txt'
            elif field == 'Product Description': template_path = f'{template_file_path}{brand.name}/{product.type}/product_description.txt'
            elif field == 'Meta Title': template_path = f'{template_file_path}{brand.name}/{product.type}/meta_title.txt'
            elif field == 'Meta Description': template_path = f'{template_file_path}{brand.name}/{product.type}/meta_description.txt'
            elif field == 'Image Description': template_path = f'{template_file_path}{brand.name}/{product.type}/image_description.txt'
            
        except Exception as e:
            self.print_logs(f'Exception in get_template_path: {e}')
            if self.DEBUG: print(f'Exception in get_template_path: {e}')
        finally: return template_path

    # get product description template
    def get_template(self, path: str) -> str:
        template = ''
        try:
            if os.path.exists(path):
                file_reader = Files_Reader(self.DEBUG)
                template = file_reader.read_text_file(path)
        except Exception as e:
            self.print_logs(f'Exception in get_template: {e}')
            if self.DEBUG: print(f'Exception in get_template: {e}')
            else: pass
        finally: return template
    
    # get original text from template
    def get_original_text(self, template: str, brand: Brand, product: Product) -> str:
        try:
            template = self.check_and_replace_text('{brand.name}', brand.name, template)
            # if '{Brand.Name}' in template: template = str(template).replace('{Brand.Name}', str(brand.name).strip().title()).strip()
            # elif '{BRAND.NAME}' in template: template = str(template).replace('{BRAND.NAME}', str(brand.name).strip().upper()).strip()
            # elif '{brand.name}' in template: template = str(template).replace('{brand.name}', str(brand.name).strip().lower()).strip()
            # template = str(template).replace('  ', ' ').strip()
            template = self.check_and_replace_text('{product.number}', product.number, template)
            # if '{Product.Number}' in template: template = str(template).replace('{Product.Number}', str(product.number).strip().title()).strip()
            # elif '{PRODUCT.NUMBER}' in template: template = str(template).replace('{PRODUCT.NUMBER}', str(product.number).strip().upper()).strip()
            # elif '{product.number}' in template: template = str(template).replace('{product.number}', str(product.number).strip().lower()).strip()
            # template = str(template).replace('  ', ' ').strip()
            template = self.check_and_replace_text('{product.name}', product.name, template)
            # if str(product.name).strip(): 
            #     if '{Product.Name}' in template: template = str(template).replace('{Product.Name}', str(product.name).strip().title())
            #     elif '{PRODUCT.NAME}' in template: template = str(template).replace('{PRODUCT.NAME}', str(product.name).strip().upper())
            #     elif '{product.name}' in template: template = str(template).replace('{product.name}', str(product.name).strip().lower())
            # else: 
            #     if '{Product.Name}' in template: template = str(template).replace('{Product.Name}', '')
            #     elif '{PRODUCT.NAME}' in template: template = str(template).replace('{PRODUCT.NAME}', '')
            #     elif '{product.name}' in template: template = str(template).replace('{product.name}', '')
            # template = str(template).replace('  ', ' ').strip()
            template = self.check_and_replace_text('{product.frame_code}', product.frame_code, template)
            # if '{Product.Frame_Code}' in template: template = str(template).replace('{Product.Frame_Code}', str(product.frame_code).strip().upper()).strip()
            # elif '{PRODUCT.FRAME_CODE}' in template: template = str(template).replace('{PRODUCT.FRAME_CODE}', str(product.frame_code).strip().upper()).strip()
            # elif '{product.frame_code}' in template: template = str(template).replace('{product.frame_code}', str(product.frame_code).strip().lower()).strip()
            # template = str(template).replace('  ', ' ').strip()
            template = self.check_and_replace_text('{product.frame_color}', product.metafields.frame_color, template)
            # if '{Product.Frame_Color}' in template: template = str(template).replace('{Product.Frame_Color}', str(product.metafields.frame_color).strip().title()).strip()
            # elif '{PRODUCT.FRAME_COLOR}' in template: template = str(template).replace('{PRODUCT.FRAME_COLOR}', str(product.metafields.frame_color).strip().upper()).strip()
            # elif '{product.frame_color}' in template: template = str(template).replace('{product.frame_color}', str(product.metafields.frame_color).strip().lower()).strip()
            # template = str(template).replace('  ', ' ').strip()
            template = self.check_and_replace_text('{product.lens_code}', product.lens_code, template)
            # if '{Product.Lens_Code}' in template: template = str(template).replace('{Product.Lens_Code}', str(product.lens_code).strip().title()).strip()
            # elif '{PRODUCT.LENS_CODE}' in template: template = str(template).replace('{PRODUCT.LENS_CODE}', str(product.lens_code).strip().upper()).strip()
            # elif '{product.lens_code}' in template: template = str(template).replace('{product.lens_code}', str(product.lens_code).strip().lower()).strip()
            # template = str(template).replace('  ', ' ').strip()
            template = self.check_and_replace_text('{product.lens_color}', product.metafields.lens_color, template)
            # if '{Product.Lens_Color}' in template: template = str(template).replace('{Product.Lens_Color}', str(product.metafields.lens_color).strip().title()).strip()
            # elif '{PRODUCT.LENS_COLOR}' in template: template = str(template).replace('{PRODUCT.LENS_COLOR}', str(product.metafields.lens_color).strip().upper()).strip()
            # elif '{product.lens_color}' in template: template = str(template).replace('{product.lens_color}', str(product.metafields.lens_color).strip().lower()).strip()
            # template = str(template).replace('  ', ' ').strip()
            template = self.check_and_replace_text('{product.type}', product.type, template)
            # if '{Product.Type}' in template: template = str(template).replace('{Product.Type}', str(product.type).strip().title()).strip()
            # elif '{PRODUCT.TYPE}' in template: template = str(template).replace('{PRODUCT.TYPE}', str(product.type).strip().upper()).strip()
            # elif '{product.type}' in template: template = str(template).replace('{product.type}', str(product.type).strip().lower()).strip()
            # template = str(template).replace('  ', ' ').strip()

            # Metafields
            template = self.check_and_replace_text('{product.metafields.for_who}', product.metafields.lens_color, template)
            # if '{Product.Metafields.For_Who}' in template: 
            #     if 'unisex' in str(product.metafields.for_who).strip().lower(): template = str(template).replace('{Product.Metafields.For_Who}', 'MEN and WOMEN').strip()
            #     else: template = str(template).replace('{Product.Metafields.For_Who}', str(product.metafields.for_who).strip().title()).strip()
            # elif '{PRODUCT.METAFIELDS.FOR_WHO}' in template:
            #     if 'unisex' in str(product.metafields.for_who).strip().lower(): template = str(template).replace('{Product.Metafields.For_Who}', 'Men and Women').strip() 
            #     else: template = str(template).replace('{PRODUCT.METAFIELDS.FOR_WHO}', str(product.metafields.for_who).strip().upper()).strip()
            # elif '{product.metafields.for_who}' in template:
            #     if 'unisex' in str(product.metafields.for_who).strip().lower(): template = str(template).replace('{Product.Metafields.For_Who}', 'men and women').strip()
            #     else: template = str(template).replace('{product.metafields.for_who}', str(product.metafields.for_who).strip().lower()).strip()
            # template = str(template).replace('  ', ' ').strip()
            template = self.check_and_replace_text('{product.metafields.lens_material}', product.metafields.lens_material, template)
            # if '{Product.Metafields.Lens_Material}' in template: template = str(template).replace('{Product.Metafields.Lens_Material}', str(product.metafields.lens_material).strip().title()).strip()
            # elif '{PRODUCT.METAFIELDS.LENS_MATERIAL}' in template: template = str(template).replace('{PRODUCT.METAFIELDS.LENS_MATERIAL}', str(product.metafields.lens_material).strip().upper()).strip()
            # elif '{product.metafields.lens_material}' in template: template = str(template).replace('{product.metafields.lens_material}', str(product.metafields.lens_material).strip().lower()).strip()
            # template = str(template).replace('  ', ' ').strip()
            template = self.check_and_replace_text('{product.metafields.lens_technology}', product.metafields.lens_technology, template)
            # if '{Product.Metafields.Lens_Technology}' in template: template = str(template).replace('{Product.Metafields.Lens_Technology}', str(product.metafields.lens_technology).strip().title()).strip()
            # elif '{PRODUCT.METAFIELDS.LENS_TECHNOLOGY}' in template: template = str(template).replace('{PRODUCT.METAFIELDS.LENS_TECHNOLOGY}', str(product.metafields.lens_technology).strip().upper()).strip()
            # elif '{product.metafields.lens_technology}' in template: template = str(template).replace('{product.metafields.lens_technology}', str(product.metafields.lens_technology).strip().lower()).strip()
            # template = str(template).replace('  ', ' ').strip()
            template = self.check_and_replace_text('{product.metafields.frame_material}', product.metafields.frame_material, template)
            # if '{Product.Metafields.Frame_Material}' in template: template = str(template).replace('{Product.Metafields.Frame_Material}', str(product.metafields.frame_material).strip().title()).strip()
            # elif '{PRODUCT.METAFIELDS.FRAME_MATERIAL}' in template: template = str(template).replace('{PRODUCT.METAFIELDS.FRAME_MATERIAL}', str(product.metafields.frame_material).strip().upper()).strip()
            # elif '{product.metafields.frame_material}' in template: template = str(template).replace('{product.metafields.frame_material}', str(product.metafields.frame_material).strip().lower()).strip()
            # template = str(template).replace('  ', ' ').strip()
            template = self.check_and_replace_text('{product.metafields.frame_shape}', product.metafields.frame_shape, template)
            # if '{Product.Metafields.Frame_Shape}' in template: template = str(template).replace('{Product.Metafields.Frame_Shape}', str(product.metafields.frame_shape).strip().title()).strip()
            # elif '{PRODUCT.METAFIELDS.FRAME_SHAPE}' in template: template = str(template).replace('{PRODUCT.METAFIELDS.FRAME_SHAPE}', str(product.metafields.frame_shape).strip().upper()).strip()
            # elif '{product.metafields.frame_shape}' in template: template = str(template).replace('{product.metafields.frame_shape}', str(product.metafields.frame_shape).strip().lower()).strip()
            # template = str(template).replace('  ', ' ').strip()

        except Exception as e:
            self.print_logs(f'Exception in get_original_text: {e}')
            if self.DEBUG: print(f'Exception in get_original_text: {e}')
            else: pass
        finally: return template
        
    def check_and_replace_text(self, text: str, value: str, template: str) -> str:
        try:
            if str(text).strip().upper() in template: 
                if str(text).strip().lower() == '{product.metafields.for_who}' and str(value).strip().lower() == 'unisex':
                    template = str(template).replace(str(text).strip().upper(), 'MEN and WOMEN')
                else: template = str(template).replace(str(text).strip().upper(), str(value).strip().upper())
            elif str(text).strip().title() in template: 
                if str(text).strip().lower() == '{product.metafields.for_who}' and str(value).strip().lower() == 'unisex':
                    template = str(template).replace(str(text).strip().title(), 'Men and Women')
                else: template = str(template).replace(str(text).strip().title(), str(value).strip().title())
            elif str(text).strip().lower() in template: 
                if str(text).strip().lower() == '{product.metafields.for_who}' and str(value).strip().lower() == 'unisex':
                    template = str(template).replace(str(text).strip().lower(), 'men and women')
                else: template = str(template).replace(str(text).strip().lower(), str(value).strip().lower())

            template = str(template).replace('  ', ' ').strip()
        except Exception as e:
            self.print_logs(f'Exception in check_and_replace_text: {e}')
            if self.DEBUG: print(f'Exception in check_and_replace_text: {e}')
            else: pass
        finally: return template

    # create product title
    def create_product_title(self, brand: Brand, product: Product, template_file_path: str) -> str:
        title = ''
        try:
            title_template_path = self.get_template_path('Product Title', brand, product, template_file_path)
            title_template = self.get_template(title_template_path)
            if title_template:
                title = self.get_original_text(title_template, brand, product)
            
            else:
                if str(brand.name).strip(): title += f'{str(brand.name).strip().title()}'
                if str(product.name).strip(): title += f' {str(product.name).strip().upper()}'
                if str(product.number).strip(): title += f' {str(product.number).strip().upper()}'
                if str(product.frame_code).strip(): title += f' {str(product.frame_code).strip().upper()}'

                title = str(title).strip()
                if '  ' in title: title = str(title).strip().replace('  ', ' ')
                if str(title).strip()[-1] == '-': title = str(title)[:-1].strip()
        except Exception as e:
            self.print_logs(f'Exception in create_product_title: {e}')
            if self.DEBUG: print(f'Exception in create_product_title: {e}')
            else: pass
        finally: return title

    # create product description
    def create_product_description(self, brand: Brand, product: Product, template_file_path: str) -> str:
        product_description = ''
        try:
            product_description_template_path = self.get_template_path('Product Description', brand, product, template_file_path)
            product_description_template = self.get_template(product_description_template_path)
            product_description = self.get_original_text(product_description_template, brand, product)
        except Exception as e:
            self.print_logs(f'Exception in create_product_description: {e}')
            if self.DEBUG: print(f'Exception in create_product_description: {e}')
        finally: return product_description

    # create product meta title
    def create_product_meta_title(self, brand: Brand, product: Product, template_file_path: str) -> str:
        meta_title = ''
        try:
            meta_title_template_path = self.get_template_path('Meta Title', brand, product, template_file_path)
            meta_title_template = self.get_template(meta_title_template_path)
            meta_title = self.get_original_text(meta_title_template, brand, product)

            if meta_title:
                meta_title = str(meta_title).replace('  ', ' ').strip()
                if len(meta_title) > 60: meta_title = str(meta_title).replace('| LookerOnline', '| LO')
        except Exception as e:
            self.print_logs(f'Exception in create_product_meta_title: {e}')
            if self.DEBUG: print(f'Exception in create_product_meta_title: {e}')
        finally: return meta_title

    # create product meta description
    def create_product_meta_description(self, brand: Brand, product: Product, template_file_path: str) -> str:
        meta_description = ''
        try:
            meta_description_template_path = self.get_template_path('Meta Description', brand, product, template_file_path)
            meta_description_template = self.get_template(meta_description_template_path)
            meta_description = self.get_original_text(meta_description_template, brand, product)

            if meta_description:
                meta_description = str(meta_description).replace('  ', ' ').replace('âœ“', '✓').strip()
        except Exception as e:
            self.print_logs(f'Exception in create_product_meta_description: {e}')
            if self.DEBUG: print(f'Exception in create_product_meta_description: {e}')
        finally: return meta_description

    # create product image description
    def create_product_image_description(self, brand: Brand, product: Product, template_file_path: str) -> str:
        image_description = ''
        try:
            image_description_template_path = self.get_template_path('Image Description', brand, product, template_file_path)
            image_description_template = self.get_template(image_description_template_path)
            image_description = self.get_original_text(image_description_template, brand, product)
        except Exception as e:
            self.print_logs(f'Exception in create_product_image_description: {e}')
            if self.DEBUG: print(f'Exception in create_product_image_description: {e}')
        finally: return image_description

    # get product tags whcih are not on shopify
    def get_product_tags(self, brand: Brand, product: Product, shopify_product_tags: list[str]) -> list[str]:
        tags = []
        try:
            if str(brand.name).strip() and str(brand.name).strip() not in shopify_product_tags: tags.append(str(brand.name).strip())
            if str(product.number).strip() and str(product.number).strip().upper() not in shopify_product_tags: tags.append(str(product.number).strip().upper())
            if str(product.name).strip() and str(product.name).strip().upper() not in shopify_product_tags: tags.append(str(product.name).strip().upper())
            if str(product.frame_code).strip() and str(product.frame_code).strip().upper() not in shopify_product_tags: tags.append(str(product.frame_code).strip().upper())
            if str(product.lens_code).strip() and str(product.lens_code).strip().upper() not in shopify_product_tags: tags.append(str(product.lens_code).strip().upper())
            if str(product.type).strip() and str(product.type).strip() not in shopify_product_tags: tags.append(str(product.type).strip())
            if str(product.metafields.for_who).strip():
                if str(product.metafields.for_who).strip().lower() == 'unisex':
                    if 'Men'  not in shopify_product_tags: tags.append('Men')
                    if 'Women'  not in shopify_product_tags: tags.append('Women')
                else:
                    if str(product.metafields.for_who).strip() not in shopify_product_tags: 
                        tags.append(str(product.metafields.for_who).strip())
            if str(product.metafields.lens_material).strip() and str(product.metafields.lens_material).strip() not in shopify_product_tags: tags.append(str(product.metafields.lens_material).strip())
            if str(product.metafields.lens_technology).strip() and str(product.metafields.lens_technology).strip() not in shopify_product_tags: tags.append(str(product.metafields.lens_technology).strip())
            if str(product.metafields.frame_shape).strip() and str(product.metafields.frame_shape).strip() not in shopify_product_tags: tags.append(str(product.metafields.frame_shape).strip())
            if str(product.metafields.frame_material).strip() and str(product.metafields.frame_material).strip() not in shopify_product_tags: tags.append(str(product.metafields.frame_material).strip())
        except Exception as e:
            self.print_logs(f'Exception in get_product_tags: {e}')
            if self.DEBUG: print(f'Exception in get_product_tags: {e}')
            else: pass
        finally: return tags

    # get new product metafields for the product
    def get_new_product_metafeilds(self, brand: Brand, product: Product,template_file_path: str) -> list[dict]:
        metafields = []
        try:
            meta_title = self.create_product_meta_title(brand, product, template_file_path)
            meta_description = self.create_product_meta_description(brand, product, template_file_path)
            if str(product.metafields.for_who).strip(): 
                metafields.append({"product_id": product.shopify_id, "namespace": "my_fields", "key": "for_who", "value": str(product.metafields.for_who).strip(), "type": "single_line_text_field"})
                metafields.append({"product_id": product.shopify_id, "namespace": "italian", "key": "per_chi", "value": str(product.metafields.for_who).strip(), "type": "single_line_text_field"})
            if str(product.metafields.frame_color).strip(): 
                metafields.append({"product_id": product.shopify_id, 'namespace': 'my_fields', 'key': 'frame_color', "value": str(product.metafields.frame_color).strip(), "type": "single_line_text_field"})
                metafields.append({"product_id": product.shopify_id, 'namespace': 'italian', 'key': 'colore_della_montatura', "value": str(product.metafields.frame_color).strip(), "type": "single_line_text_field"})
            if str(product.metafields.frame_material).strip(): 
                metafields.append({"product_id": product.shopify_id, 'namespace': 'my_fields', 'key': 'frame_material', "value": str(product.metafields.frame_material).strip(), "type": "single_line_text_field"})
                metafields.append({"product_id": product.shopify_id, 'namespace': 'italian', 'key': 'materiale_della_montatura', "value": str(product.metafields.frame_material).strip(), "type": "single_line_text_field"})
            if str(product.metafields.frame_shape).strip(): 
                metafields.append({"product_id": product.shopify_id, 'namespace': 'my_fields', 'key': 'frame_shape', "value": str(product.metafields.frame_shape).strip(), "type": "single_line_text_field"})
                metafields.append({"product_id": product.shopify_id, 'namespace': 'italian', 'key': 'forma', "value": str(product.metafields.frame_shape).strip(), "type": "single_line_text_field"})
            if str(product.metafields.lens_color).strip(): 
                metafields.append({"product_id": product.shopify_id, 'namespace': 'my_fields', 'key': 'lens_color', "value": str(product.metafields.lens_color).strip(), "type": "single_line_text_field"})
                metafields.append({"product_id": product.shopify_id, 'namespace': 'italian', 'key': 'colore_della_lente', "value": str(product.metafields.lens_color).strip(), "type": "single_line_text_field"})
            if str(product.metafields.lens_material).strip(): 
                metafields.append({"product_id": product.shopify_id, 'namespace': 'my_fields', 'key': 'lens_material', "value": str(product.metafields.lens_material).strip(), "type": "single_line_text_field"})
                metafields.append({"product_id": product.shopify_id, 'namespace': 'italian', 'key': 'materiale_della_lente', "value": str(product.metafields.lens_material).strip(), "type": "single_line_text_field"})
            if str(product.metafields.lens_technology).strip(): 
                metafields.append({"product_id": product.shopify_id, 'namespace': 'my_fields', 'key': 'lens_technology', "value": str(product.metafields.lens_technology).strip(), "type": "single_line_text_field"})
                metafields.append({"product_id": product.shopify_id, 'namespace': 'italian', 'key': 'tecnologia_della_lente', "value": str(product.metafields.lens_technology).strip(), "type": "single_line_text_field"})
            if str(product.metafields.size_bridge_template).strip(): 
                metafields.append({"product_id": product.shopify_id, 'namespace': 'my_fields', 'key': 'product_size', "value": str(product.metafields.size_bridge_template).strip(), "type": "single_line_text_field"})
                metafields.append({"product_id": product.shopify_id, 'namespace': 'italian', 'key': 'calibro_ponte_asta', "value": str(product.metafields.size_bridge_template).strip(), "type": "single_line_text_field"})
            if str(product.metafields.gtin1).strip(): 
                metafields.append({"product_id": product.shopify_id, 'namespace': 'my_fields', 'key': 'gtin1', "value": str(product.metafields.gtin1).strip(), "type": "single_line_text_field"})
            if str(meta_title).strip(): metafields.append({"product_id": product.shopify_id, 'namespace': 'global', 'key': 'title_tag', "value": str(meta_title).strip(), "type": "single_line_text_field"}) 
            if str(meta_description).strip(): metafields.append({"product_id": product.shopify_id, 'namespace': 'global', 'key': 'description_tag', "value": str(meta_description).strip(), "type": "single_line_text_field"})
            
        except Exception as e: 
            self.print_logs(f'Exception in get_new_product_metafeilds: {e}')
            if self.DEBUG: print(f'Exception in get_new_product_metafeilds: {e}')
            else: pass
        finally: return metafields

    # add 360 images to the product on shopify
    def add_product_360_images(self, store_name: str, product: Product, image_description: str, shopify_processor: Shopify_Processor) -> None:
        try:
            if str(store_name).strip().title() == 'Digitalhub':
                img_360_urls = product.images_360

                if '_08.' in img_360_urls[-1]:
                    last_image = img_360_urls.pop(-1)
                    img_360_urls.insert(0, last_image)

                for index, image_360_url in enumerate(img_360_urls):
                    image_filename = ''
                    image_filename = str(image_360_url).strip().split('/')[-1].strip()
                    if image_filename:
                        image_attachment = self.download_image(image_360_url)
                        if image_attachment:
                            # save downloaded image
                            with open(image_filename, 'wb') as f: f.write(image_attachment)
                            # crop image to the correct size
                            self.crop_downloaded_image(image_filename)
                            # open croped image
                            f = open(image_filename, 'rb')
                            image_attachment = base64.b64encode(f.read())
                            f.close()

                            json_value = {"image": {"position": index + 1, "attachment": image_attachment.decode('utf-8'), "filename": image_filename, "alt": image_description}}
                            shopify_processor.set_product_image(product.shopify_id, json_value)
                            # delete downloaded image
                            os.remove(image_filename)
            elif str(store_name).strip().title() == 'Safilo':
                for index, image_360_url in enumerate(product.images_360):
                    image_filename = ''
                    image_360_url = str(image_360_url).strip()
                    image_filename = f'{str(image_description).replace(" ", "_")}__{index + 1}.jpg'
                    if image_filename:
                        json_value = {"image": {"position": index + 1, "src": image_360_url, "filename": image_filename, "alt": image_description}}
                        shopify_processor.set_product_image(product.shopify_id, json_value)
            elif str(store_name).strip().title() == 'Keringeyewear':
                for index, image_360_url in enumerate(product.images_360):
                    image_filename = f"{str(image_description).strip().replace(' ', '_')}.png"
                    json_value = {"image": {"position": index + 1, "src": image_360_url, "filename": image_filename, "alt": image_description}}
                    shopify_processor.set_product_image(product.shopify_id, json_value)
            elif str(store_name).strip().title() == 'Rudyproject': print('Rudyproject')
            elif str(store_name).strip().title() == 'Luxottica':
                for index, image_360_url in enumerate(product.images_360):
                    image_360_url = str(image_360_url).strip()
                    if '?impolicy=' in image_360_url: image_360_url = str(image_360_url).split('?impolicy=')[0].strip()
                    
                    image_filename = image_360_url.split('/')[-1].strip()

                    if '?' in image_filename: image_filename = str(image_filename).split('?')[0].strip()
                    if image_filename[0] == '0': image_filename = image_filename[1:]

                    if image_filename:
                        json_value = {"image": {"position": index + 1, "src": image_360_url, "filename": image_filename, "alt": image_description}}
                        if not shopify_processor.set_product_image(product.shopify_id, json_value):
                            image_attachment = self.download_image(image_360_url)
                            if image_attachment:
                                # save downloaded image
                                with open(image_filename, 'wb') as f: f.write(image_attachment)
                                # open croped image
                                f = open(image_filename, 'rb')
                                image_attachment = base64.b64encode(f.read())
                                f.close()
                                
                                json_value = {"image": {"position": index + 1, "attachment": image_attachment.decode('utf-8'), "filename": image_filename, "alt": image_description}}
                                shopify_processor.set_product_image(product.shopify_id, json_value)
                                # delete downloaded image
                                os.remove(image_filename)
                            else: self.print_logs(f'')
        except Exception as e:
            self.print_logs(f'Exception in add_product_360_images: {e}')
            if self.DEBUG: print(f'Excepption in add_product_360_images: {e}')
            else: pass
    
    # check spin image tag for product
    def check_product_spin_tag(self, num_images: int, tags_str: str) -> str:
        tags = []
        try:
            # Split the tags_str into a list of tags
            tags = tags_str.split(",")
            
            # Check if the spinimages tag is already present in the tags list
            spin_tag_present = any(str(tag).strip().startswith("spinimages=") for tag in tags)
            
            if spin_tag_present:
                exact_spin_tag_present = False
                for tag in tags:
                    if f'spinimages={num_images}' == str(tag).strip(): 
                        exact_spin_tag_present = True
                        break
                if not exact_spin_tag_present: tags.append(f'spinimages={num_images}')

                duplicate_tags = []
                for tag in tags:
                    if str(tag).strip().startswith('spinimages') and str(tag).strip() != f'spinimages={num_images}':
                        duplicate_tags.append(tag)

                if duplicate_tags:
                    tags = [string for string in tags if string not in duplicate_tags]
            else: tags.append(f'spinimages={num_images}')
            
            if tags == tags_str.split(','): tags = []
        except Exception as e:
            self.print_logs(f'Exception in check_product_spin_tag: {e}')
            if self.DEBUG: print(f'Excepption in check_product_spin_tag: {e}')
            else: pass
        finally: return ",".join(tags)
    
    # remove spin tag from tags
    def remove_spin_tag(self, tags: str):
        new_tags = []
        try:
            for tag in str(tags).split(','):
                if 'spinimages' not in str(tag).strip().lower():
                    new_tags.append(str(tag).strip())
        except Exception as e:
            self.print_logs(f'Exception in remove_spin_tag: {e}')
            if self.DEBUG: print(f'Excepption in remove_spin_tag: {e}')
            else: pass
        finally: return ', '.join(new_tags)

    # add product image to the shopify
    def add_product_image(self, store_name: str, product: Product, image_description: str, shopify_processor: Shopify_Processor) -> None:
        try:
            if str(store_name).strip().title() == 'Digitalhub': print('Digitalhub')
            elif str(store_name).strip().title() == 'Safilo': print('Safilo')
            elif str(store_name).strip().title() == 'Keringeyewear': print('Keringeyewear')
            elif str(store_name).strip().title() == 'Rudyproject': print('Rudyproject')
            elif str(store_name).strip().title() == 'Luxottica':
                image = str(product.image).strip()
                if '?impolicy=' in image: image = str(image).split('?impolicy=')[0].strip()
                
                image_filename = image.split('/')[-1].strip()
                if '?' in image_filename: image_filename = str(image_filename).split('?')[0].strip()
                if image_filename[0] == '0': image_filename = image_filename[1:]
                
                if image_filename:
                    json_value = {"image": {"position": 1, "src": image, "filename": image_filename, "alt": image_description}}
                    shopify_processor.set_product_image(product.shopify_id, json_value)
            # image_attachment = shopify_processor.download_image(str(product.image).strip())
            # if image_attachment:
            #     image_attachment = base64.b64encode(image_attachment)
            #     image_filename = str(product.image).strip().split('/')[-1].strip()
            #     json_value = {"image": {"position": 1, "attachment": image_attachment.decode('utf-8'), "filename": image_filename, "alt": image_description}}
            #     if not shopify_processor.update_product_image(product.shopify_id, json_value):
            #         self.print_logs(f'Failed to update product: {product.shopify_id} image')
            # else: self.print_logs(f'Failed to download image for {product.number} {product.frame_code}')
        except Exception as e:
            self.print_logs(f'Exception in add_product_image: {e}')
            if self.DEBUG: print(f'Excepption in add_product_image: {e}')
            else: pass

    # print logs to the log file
    def print_logs(self, log: str):
        try:
            with open(self.logs_filename, 'a') as f:
                f.write(f'\n{log}')
        except: pass


    def crop_downloaded_image(self, filename: str) -> None:
        try:
            im = Image.open(filename)
            width, height = im.size   # Get dimensions
            new_width = 1680
            new_height = 1020
            left = (width - new_width)/2
            top = (height - new_height)/2
            right = (width + new_width)/2
            bottom = (height + new_height)/2
            im = im.crop((left, top, right, bottom))
            try:
                im.save(filename)
            except:
                rgb_im = im.convert('RGB')
                rgb_im.save(filename)
        except Exception as e:
            if self.DEBUG: print(f'Exception in crop_downloaded_image: {e}')
            self.print_logs(f'Exception in crop_downloaded_image: {e}')

    # this function will download image from the given url
    def download_image(self, url: str):
        image_attachment = ''
        try:
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-Encoding': 'gzip, deflate, br',
                'accept-Language': 'en-US,en;q=0.9',
                'cache-Control': 'max-age=0',
                'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'Sec-Fetch-User': '?1',
                'upgrade-insecure-requests': '1',
            }
            
            for _ in range(0, 10):
                try:
                    response = requests.get(url=url, headers=headers, stream=True)
                    if response.status_code == 200:
                        # image_attachment = base64.b64encode(response.content)
                        image_attachment = response.content
                        break
                    elif response.status_code == 404: 
                        self.print_logs(f'404 in downloading this image {url}')
                        break
                    else: 
                        self.print_logs(f'{response.status_code} found for downloading image')
                        sleep(1)
                except: pass
        except Exception as e:
            if self.DEBUG: print(f'Exception in download_image: {str(e)}')
            self.print_logs(f'Exception in download_image: {str(e)}')
        finally: return image_attachment
