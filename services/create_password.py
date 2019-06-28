import random,string
def GetPassword(length):
  Ofnum=random.randint(1,length)
  Ofletter=length-Ofnum
  slcNum=[random.choice(string.digits) for i in range(Ofnum)]
  slcLetter=[random.choice(string.ascii_letters) for i in range(Ofletter)]
  slcChar=slcLetter+slcNum
  random.shuffle(slcChar)
  pwd=''.join([i for i in slcChar])
  return pwd

if __name__=='__main__':
  print( GetPassword(10))