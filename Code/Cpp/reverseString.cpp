// g++ -o a.out reverseString.cpp stringBuffer.cpp

#include <iostream>
#include "stringBuffer.h"

using namespace std;

int main(){

  string_buffer sb (10);
  
  sb.append("abcdefG", 7);
  cout << sb.get_char_array() << "\n";
  sb.rev();
  cout << sb.get_char_array() << "\n";

  return 0;
}
