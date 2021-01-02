import scrapy
import logging


class JkmkprojectSpider(scrapy.Spider):
    name = 'jkmkproject'
    allowed_domains = ['www.beatport.com']

    url_list=[]

    #while True:
	#    url2= str(input("Pega los enlaces de los albunes aqui y escribe 'ya' cuando termines: "))
	#    if url2 == "ya":
#		    break
#	    else:
#	    	url_list.append(url2)
            
    start_urls = url= (str(input("Pega los enlaces de los albunes aqui y escribe 'ya' cuando termines: ")).split(","))
    
#3199108
    #custom_settings = {
    #'CLOSESPIDER_PAGECOUNT': 40,

     #}


    def release_date(self, texto):
        a= "RELEASE DATE "
        x="\n"
        b=a+texto+x
        return b

    def catalog(self, texto):
        a= "CATALOG "
        x="\n \n"
        b=' [wpmem_logged_in]/ <strong><a href="OD" rel="noopener"><span style="color: #02bd32;">ZIP</span></a></strong>[/wpmem_logged_in] \n \n <strong><span style="color: #f5a614;">Download AIFF:</span></strong> \n \n \n <strong><span style="color: #f5a614;">Download MP3:</span></strong>'
        c=a+texto+b+x
        return c 


    def label(self, texto):
        a= "LABEL "
        x="\n"
        b=a+texto+x
        return b


    def plantilla_script(self, texto):

        b='[bg_collapse view="link" color="#adadad" icon="arrow" expand_text="Pre-listen:" collapse_text="Show Less" ]'
        c= ' [/bg_collapse]'
        d=b+texto+c
        return d


    def autores(self,text):

        if type(text) ==list:

            nombres=", ".join(text)

        else:
            nombres= text

        return nombres

    def parse(self, response):
        
        catalogo=response.xpath("(//li[@class='interior-release-chart-content-item interior-release-chart-content-item--small interior-release-chart-content-item--mobile'])[3]/span[2]/text()").get()
        
        links_list=response.xpath("(//p[@class='buk-track-title']/a)[1]")

        for link in links_list:

            links= link.xpath("./@href").get()

            #absolute_url=response.urljoin(links)

            yield response.follow(url=links, callback=self.parse_songs, meta={"catalogo":catalogo})

    def parse_songs(self,response):

        catalogo_id=self.catalog(response.request.meta["catalogo"])

        fecha_lanzamiento=self.release_date(response.xpath("//li[@class='interior-track-content-item interior-track-released']/span[2]/text()").get())

        label=self.label(response.xpath("//li[@class='interior-track-content-item interior-track-labels']/span[2]/a/text()").get())

        nombre_pista= response.xpath("(//div[@class='interior-title'])[1]/h1[1]/text()").get()

        codigo_script= self.plantilla_script(response.xpath("(//input[@class='share-embed-drop-copy-text'])[2]/@value").get())

        album= response.xpath("//li[@class='interior-track-releases-artwork-container ec-item']/@data-ec-name").get()

        nombre_autores=self.autores(response.xpath("//div[@class='interior-track-artists']/span[@class='value']/a/text()").getall())

        plantilla=fecha_lanzamiento+label+catalogo_id+codigo_script

        
        yield {
            
           
            "nombre de la pista": nombre_pista,
    
            "album": album,
            "nombre de los autores": nombre_autores,
            "plantilla a copiar": plantilla
        }



        
