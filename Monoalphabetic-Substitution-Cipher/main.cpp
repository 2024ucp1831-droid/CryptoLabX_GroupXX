#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <cctype>
using namespace std;

void frequency_analysis(string ciphertext)
{
    int frequency[26]={0};
    int total=0;

    for(int i=0;i<ciphertext.length();i++)
    {
        if(isalpha(ciphertext[i]))
        {
            char ch=toupper(ciphertext[i]);
            frequency[ch-'A']++;
            total++;
        }
    }

    cout<<"\n========== LETTER FREQUENCY ANALYSIS ==========\n";
    cout<<"\nLetter\tCount\tPercentage\n";

    for(int i=0;i<26;i++)
    {
        if(frequency[i]>0)
        {
            double percentage=(frequency[i]*100.0)/total;
            cout<<char('A'+i)<<"\t"<<frequency[i]<<"\t"<<percentage<<"%\n";
        }
    }

    cout<<"\nLetters in descending frequency:\n";

    int temp[26];

    for(int i=0;i<26;i++)
        temp[i]=frequency[i];

    for(int count=0;count<26;count++)
    {
        int largest=-1;
        int position=-1;

        for(int i=0;i<26;i++)
        {
            if(temp[i]>largest)
            {
                largest=temp[i];
                position=i;
            }
        }

        if(largest>0)
        {
            cout<<char('A'+position)<<" ";
            temp[position]=-1;
        }
    }

    int largest=0;
    char mostFrequent='-';

    for(int i=0;i<26;i++)
    {
        if(frequency[i]>largest)
        {
            largest=frequency[i];
            mostFrequent=char('A'+i);
        }
    }

    cout<<"\n\nMost frequent letter: "<<mostFrequent<<"\n";
}

void word_frequency_analysis(string ciphertext)
{
    map<string,int> wordCount;
    string word="";

    for(int i=0;i<=ciphertext.length();i++)
    {
        if(i<ciphertext.length()&&isalpha(ciphertext[i]))
            word+=toupper(ciphertext[i]);
        else
        {
            if(word.length()>0)
            {
                wordCount[word]++;
                word="";
            }
        }
    }

    cout<<"\n========== WORD FREQUENCY ANALYSIS ==========\n";

    cout<<"\nRepeated words:\n";

    for(auto item:wordCount)
    {
        if(item.second>1)
            cout<<item.first<<" -> "<<item.second<<" times\n";
    }

    cout<<"\nOne-letter words:\n";

    for(auto item:wordCount)
    {
        if(item.first.length()==1)
            cout<<item.first<<" -> "<<item.second<<" times\n";
    }

    cout<<"\nTwo-letter words:\n";

    for(auto item:wordCount)
    {
        if(item.first.length()==2)
            cout<<item.first<<" -> "<<item.second<<" times\n";
    }

    cout<<"\nThree-letter words:\n";

    for(auto item:wordCount)
    {
        if(item.first.length()==3)
            cout<<item.first<<" -> "<<item.second<<" times\n";
    }
}

string get_pattern(string word)
{
    char letters[26];
    int numbers[26];
    int count=0;
    string pattern="";

    for(int i=0;i<word.length();i++)
    {
        bool found=false;

        for(int j=0;j<count;j++)
        {
            if(letters[j]==word[i])
            {
                pattern+=char('0'+numbers[j]);
                found=true;
                break;
            }
        }

        if(!found)
        {
            letters[count]=word[i];
            numbers[count]=count;
            pattern+=char('0'+count);
            count++;
        }
    }

    return pattern;
}

void pattern_analysis(string ciphertext)
{
    map<string,int> patternCount;
    string word="";

    cout<<"\n========== PATTERN ANALYSIS ==========\n";

    for(int i=0;i<=ciphertext.length();i++)
    {
        if(i<ciphertext.length()&&isalpha(ciphertext[i]))
            word+=toupper(ciphertext[i]);
        else
        {
            if(word.length()>0)
            {
                string pattern=get_pattern(word);
                cout<<word<<" -> "<<pattern<<"\n";
                patternCount[pattern]++;
                word="";
            }
        }
    }

    cout<<"\nRepeated patterns:\n";

    for(auto item:patternCount)
    {
        if(item.second>1)
            cout<<item.first<<" -> "<<item.second<<" times\n";
    }
}

string apply_substitution(string ciphertext,map<char,char> key)
{
    string result="";

    for(int i=0;i<ciphertext.length();i++)
    {
        char ch=ciphertext[i];

        if(isalpha(ch))
        {
            char upper=toupper(ch);

            if(key.find(upper)!=key.end())
                result+=key[upper];
            else
                result+='_';
        }
        else
            result+=ch;
    }

    return result;
}

void display_partial_plaintext(string ciphertext,map<char,char> key)
{
    cout<<"\nPartial plaintext:\n";
    cout<<apply_substitution(ciphertext,key)<<"\n";
}

bool valid_substitution(map<char,char> key,char cipher,char plain)
{
    for(auto item:key)
    {
        if(item.first!=cipher&&item.second==plain)
            return false;
    }

    return true;
}

string encrypt_text(string plaintext,string key)
{
    string ciphertext="";

    for(int i=0;i<plaintext.length();i++)
    {
        char ch=plaintext[i];

        if(isalpha(ch))
        {
            char encrypted=key[toupper(ch)-'A'];

            if(islower(ch))
                encrypted=tolower(encrypted);

            ciphertext+=encrypted;
        }
        else
            ciphertext+=ch;
    }

    return ciphertext;
}

string reencrypt(string plaintext,map<char,char> key)
{
    string result="";

    for(int i=0;i<plaintext.length();i++)
    {
        char ch=plaintext[i];

        if(isalpha(ch))
        {
            char upper=toupper(ch);
            char encrypted='?';

            for(auto item:key)
            {
                if(item.second==upper)
                {
                    encrypted=item.first;
                    break;
                }
            }

            if(islower(ch))
                encrypted=tolower(encrypted);

            result+=encrypted;
        }
        else
            result+=ch;
    }

    return result;
}

void display_key(map<char,char> key)
{
    cout<<"\n========== RECOVERED SUBSTITUTION KEY ==========\n";
    cout<<"Cipher -> Plain\n";

    for(auto item:key)
        cout<<item.first<<" -> "<<item.second<<"\n";
}

int main()
{
    ifstream file("attack.txt");

    if(!file)
    {
        cout<<"ERROR: attack.txt not found!\n";
        return 0;
    }

    string plaintext="";
    string line;

    while(getline(file,line))
    {
        plaintext+=line;
        plaintext+="\n";
    }

    file.close();

    string encryptionKey;

    cout<<"Enter 26-letter substitution key: ";
    cin>>encryptionKey;

    for(int i=0;i<encryptionKey.length();i++)
        encryptionKey[i]=toupper(encryptionKey[i]);

    if(encryptionKey.length()!=26)
    {
        cout<<"ERROR: Key must contain 26 letters.\n";
        return 0;
    }

    string ciphertext=encrypt_text(plaintext,encryptionKey);

    cout<<"\n========== CIPHERTEXT ==========\n";
    cout<<ciphertext<<"\n";

    frequency_analysis(ciphertext);
    word_frequency_analysis(ciphertext);
    pattern_analysis(ciphertext);

    cout<<"\n========== CANDIDATE SUBSTITUTIONS ==========\n";
    cout<<"\nCommon English frequency order:\n";
    cout<<"E T A O I N S H R D L U\n";

    map<char,char> recoveredKey;

    cout<<"\n========== ITERATIVE CRYPTANALYSIS ==========\n";
    cout<<"\nEnter substitution as: Q E\n";
    cout<<"Enter X X when finished.\n";

    while(true)
    {
        char cipherLetter,plainLetter;

        cout<<"\nEnter substitution: ";
        cin>>cipherLetter>>plainLetter;

        cipherLetter=toupper(cipherLetter);
        plainLetter=toupper(plainLetter);

        if(cipherLetter=='X'&&plainLetter=='X')
            break;

        if(!isalpha(cipherLetter)||!isalpha(plainLetter))
        {
            cout<<"Please enter letters only.\n";
            continue;
        }

        if(!valid_substitution(recoveredKey,cipherLetter,plainLetter))
        {
            cout<<"INVALID SUBSTITUTION!\n";
            continue;
        }

        recoveredKey[cipherLetter]=plainLetter;

        cout<<"\nSubstitution tested: "
            <<cipherLetter<<" -> "<<plainLetter<<"\n";

        display_partial_plaintext(ciphertext,recoveredKey);

        cout<<"\n1. Keep\n";
        cout<<"2. Reject\n";
        cout<<"3. Continue\n";

        int choice;
        cin>>choice;

        if(choice==2)
        {
            recoveredKey.erase(cipherLetter);
            cout<<"\nSubstitution rejected.\n";
            display_partial_plaintext(ciphertext,recoveredKey);
        }
    }

    display_key(recoveredKey);

    cout<<"\n========== RECOVERED PLAINTEXT ==========\n";

    string recoveredPlaintext=
        apply_substitution(ciphertext,recoveredKey);

    cout<<recoveredPlaintext<<"\n";

    cout<<"\n========== VERIFICATION ==========\n";

    cin.ignore();

    cout<<"Enter final recovered plaintext:\n";

    string finalPlaintext;
    getline(cin,finalPlaintext);

    string checkCiphertext=
        reencrypt(finalPlaintext,recoveredKey);

    cout<<"\nRe-encrypted ciphertext:\n";
    cout<<checkCiphertext<<"\n";

    if(checkCiphertext==ciphertext)
        cout<<"\nSUCCESS! Plaintext is VERIFIED.\n";
    else
        cout<<"\nVERIFICATION FAILED.\n";

    return 0;
}
