#Initiating the list modern_family
modern_family = ['CLaiRe_DunPhY', 'PHiL_dUnpHY', 'GLoRiA_PriTCheTt', 'CaMErOn_TuCKEr','StELLa']

#enumerate and appending
indices=[index  for index,y in enumerate(modern_family)]
characters=[]

for item in modern_family:
    characters.append(item)
list(enumerate(indices))
list(enumerate(characters))

#Converting all into lower case
characters = [element.lower() for element in characters]

#Replacing '_' with ','
characters = [element.replace("_","-") for element in characters]

#Mapping by lamda and finding the length of the input sequence
temp=[]
temp = (map(lambda x:len(x),characters))

#Adding indices and temp and then zipping it
indices = [sum(i) for i in zip(indices, temp )]  
indices.sort(reverse=True)

#Printing final lists
print(indices)
print(characters)

#Creating a dictonary using indices as keys and characters are values
Phew_finally = {}
for key in indices:
    for value in characters:
        Phew_finally[key] = value
        characters.remove(value)
        break

print(Phew_finally)
