cities = ["Porto Velho", "Nova Mamoré", "Buritis", "Candeias do Jamari", "Costa Marques", "Guajará-Mirim",
    "São Francisco do Guaporé", "Cacaulândia", "Vale do Anari", "Jaru", "Ji-Paraná", "Ouro Preto do Oeste",
    "Presidente Médici", "Mirante da Serra", "Nova União", "Teixeirópolis", "Urupá", "Vale do Paraíso",
    "Nova Brasilândia D'Oeste", "São Miguel do Guaporé", "Seringueiras", "Alta Floresta D'Oeste", "Cacoal",
    "Espigão D'Oeste", "Castanheiras", "Chupinguaia", "Cabixi", "Pimenteiras do Oeste", "Cruzeiro do Sul",
    "Mâncio Lima", "Marechal Thaumaturgo", "Porto Walter", "Rodrigues Alves", "Feijó", "Jordão", "Tarauacá",
    "Manoel Urbano", "Santa Rosa do Purus", "Sena Madureira", "Acrelândia", "Bujari", "Capixaba", "Plácido de Castro",
    "Rio Branco", "Senador Guiomard", "Porto Acre", "Assis Brasil", "Brasiléia", "Epitaciolândia", "Xapuri",
    "Barcelos", "Novo Airão", "Santa Isabel do Rio Negro", "São Gabriel da Cachoeira", "Japurá", "Maraã", "Amaturá",
    "Atalaia do Norte", "Benjamin Constant", "Fonte Boa", "Jutaí", "Santo Antônio do Içá", "São Paulo de Olivença",
    "Tabatinga", "Tonantins", "Carauari", "Eirunepé", "Envira", "Guajará", "Ipixuna", "Itamarati", "Juruá",
    "Alvarães", "Tefé", "Uarini", "Anamã", "Anori", "Beruri", "Caapiranga", "Coari", "Codajás", "Autazes", "Careiro",
    "Iranduba", "Manacapuru", "Manaquiri", "Manaus", "Presidente Figueiredo", "Rio Preto da Eva", "Itacoatiara",
    "Itapiranga", "Nova Olinda do Norte", "Silves", "Urucurituba", "Barreirinha", "Boa Vista do Ramos", "Maués",
    "Nhamundá", "Parintins", "São Sebastião do Uatumã", "Urucará", "Boca do Acre", "Pauini", "Canutama", "Lábrea",
    "Tapauá", "Apuí", "Borba", "Humaitá", "Manicoré", "Novo Aripuanã", "Caracaraí", "Caroebe", "Rorainópolis",
    "São João da Baliza", "São Luiz", "Faro", "Juruti", "Óbidos", "Oriximiná", "Terra Santa", "Alenquer", "Belterra",
    "Curuá", "Mojuí dos Campos", "Monte Alegre", "Placas", "Prainha", "Santarém", "Almeirim", "Bagre", "Gurupá",
    "Melgaço", "Portel", "Afuá", "Anajás", "Breves", "Curralinho", "São Sebastião da Boa Vista", "Cachoeira do Arari",
    "Chaves", "Muaná", "Ponta de Pedras", "Santa Cruz do Arari", "Ananindeua", "Barcarena", "Belém", "Benevides",
    "Marituba", "Santa Bárbara do Pará", "Bujaru", "Inhangapi", "Santa Isabel do Pará", "Santo Antônio do Tauá",
    "Colares", "Curuçá", "Magalhães Barata", "Maracanã", "Marapanim", "Salinópolis", "São Caetano de Odivelas",
    "São João da Ponta", "São João de Pirabas", "Terra Alta", "Vigia", "Augusto Corrêa", "Bonito", "Bragança",
    "Capanema", "Igarapé-Açu", "Nova Timboteua", "Peixe-Boi", "Primavera", "Quatipuru", "Santa Maria do Pará",
    "Santarém Novo", "São Francisco do Pará", "Tracuateua", "Abaetetuba", "Baião", "Cametá", "Igarapé-Miri",
    "Limoeiro do Ajuru", "Mocajuba", "Oeiras do Pará", "Acará", "Moju", "Tailândia", "Tomé-Açu", "Cachoeira do Piriá",
    "Capitão Poço", "Garrafão do Norte", "Irituia", "Nova Esperança do Piriá", "Ourém", "Santa Luzia do Pará",
    "São Domingos do Capim", "São Miguel do Guamá", "Viseu", "Aveiro", "Itaituba", "Jacareacanga", "Novo Progresso",
    "Rurópolis", "Trairão", "Altamira", "Anapu", "Brasil Novo", "Medicilândia", "Pacajá", "Senador José Porfírio",
    "Uruará", "Vitória do Xingu", "Breu Branco", "Itupiranga", "Jacundá", "Nova Ipixuna", "Novo Repartimento",
    "Tucuruí", "Bom Jesus do Tocantins", "Goianésia do Pará", "Bannach", "Cumaru do Norte", "Ourilândia do Norte",
    "São Félix do Xingu", "Água Azul do Norte", "Canaã dos Carajás", "Curionópolis", "Eldorado dos Carajás",
    "Parauapebas", "Brejo Grande do Araguaia", "Marabá", "São Domingos do Araguaia", "São João do Araguaia",
    "Piçarra", "São Geraldo do Araguaia", "Xinguara", "Calçoene", "Oiapoque", "Amapá", "Pracuúba", "Tartarugalzinho", "Serra do Navio",
    "Pedra Branca do Amapari", "Cutias", "Ferreira Gomes", "Itaubal", "Macapá", "Porto Grande", "Santana",
    "Laranjal do Jari", "Mazagão", "Vitória do Jari", "Alcântara", "Apicum-Açu", "Bacuri", "Cedral",
    "Central do Maranhão", "Cururupu", "Guimarães", "Mirinzal", "Porto Rico do Maranhão", "Serrano do Maranhão",
    "Paço do Lumiar", "São José de Ribamar", "São Luís", "Axixá", "Bacabeira", "Cachoeira Grande", "Icatu",
    "Morros", "Presidente Juscelino", "Rosário", "Santa Rita", "Barreirinhas", "Humberto de Campos",
    "Primeira Cruz", "Santo Amaro do Maranhão", "Anajatuba", "Arari", "Bela Vista do Maranhão", "Cajari",
    "Igarapé do Meio", "Matinha", "Monção", "Olinda Nova do Maranhão", "Palmeirândia", "Pedro do Rosário",
    "Penalva", "Peri Mirim", "Pinheiro", "Presidente Sarney", "Santa Helena", "São Bento", "São João Batista",
    "São Vicente Ferrer", "Viana", "Vitória do Mearim", "Itapecuru Mirim", "Amapá do Maranhão",
    "Boa Vista do Gurupi", "Cândido Mendes", "Carutapera", "Centro do Guilherme", "Centro Novo do Maranhão",
    "Godofredo Viana", "Governador Nunes Freire", "Junco do Maranhão", "Luís Domingues", "Maracaçumé",
    "Maranhãozinho", "Turiaçu", "Alto Alegre do Pindaré", "Araguanã", "Governador Newton Bello",
    "Nova Olinda do Maranhão", "Pindaré-Mirim", "Presidente Médici", "Santa Inês", "Santa Luzia do Paruá",
    "São João do Carú", "Tufilândia", "Amarante do Maranhão", "Cidelândia", "Imperatriz",
    "São Pedro da Água Branca", "Vila Nova dos Martírios", "Aripuanã", "Brasnorte", "Castanheira",
    "Colniza", "Cotriguaçu", "Juína", "Juruena", "Rondolândia", "Alta Floresta", "Apiacás",
    "Nova Bandeirantes", "Paranaíta", "Nova Monte Verde", "Guarantã do Norte", "Terra Nova do Norte",
    "Juara", "Novo Horizonte do Norte", "Tabaporã", "Itaúba", "Nova Santa Helena",
]

import geocoder
import pandas as pd

# Initialize lists to store city names, latitudes, longitudes, and indicators
city_names = []
latitudes = []
longitudes = []
indicators = []
states = ["Rondônia","Acre","Amazonas","Roraima","Pará","Amapá","Maranhão", "Mato Grosso"]
states_now = "Rondônia"
# Loop through each city in the list
for city in cities:
    # Retrieve geolocation data for the city
    if city == "Cruzeiro do Sul":
      states_now = "Acre"
    elif city == "Barcelos":
      states_now = "Amazonas"
    elif city == "Normandia":
      states_now = "Roraima"
    elif city == "Faro":
      states_now = "Pará"
    elif city == "Calçoene":
      states_now = "Amapá"
    elif city == "Alcântara":
      states_now = "Maranhão"
    elif city == "Aripuanã":
      states_now = "Mato Gross"
      
    print(str(city)+" " + str(states_now))
    g = geocoder.bing(str(city)+ ", " + str(states_now)+ ", Brazil", key='DinjjAI58J0b7ycvFn7r~89PMoU-ZMiY-JA9mp6H2xw~AlCLNL-F_uprGVLwRL-_Hkw9yy2RUDN_ZeY0m8rvPeFGbBVrXLTbMUZfEIS3NKlv')
    
    # Check if the response is valid
    if g is not None:
        # Extract latitude and longitude from the geolocation result
        lat = g.json['lat']
        lng = g.json['lng']
        
        # Append city name, latitude, and longitude to respective lists
        city_names.append(city)
        latitudes.append(lat)
        longitudes.append(lng)
        indicators.append("Found")
    else:
        # If the response is None, mark the city as not found
        city_names.append(city)
        latitudes.append(None)
        longitudes.append(None)
        indicators.append("Not Found")

# Create a DataFrame using pandas
df = pd.DataFrame({
    'City': city_names,
    'Latitude': latitudes,
    'Longitude': longitudes,
    'Indicator': indicators
})

# Export the DataFrame to an Excel file
df.to_excel('Location.xlsx', index=False)
