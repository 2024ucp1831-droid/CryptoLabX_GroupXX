#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <cctype>

using namespace std;

vector<vector<char>> generate_key_matrix(string keyword) {
    string alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ";
    string key = "";

    for (char ch : keyword) {
        ch = toupper(ch);
        if (ch == 'J')
            ch = 'I';

        if (alphabet.find(ch) != string::npos &&
            key.find(ch) == string::npos) {
            key += ch;
        }
    }

    for (char ch : alphabet) {
        if (key.find(ch) == string::npos)
            key += ch;
    }

    vector<vector<char>> matrix(5, vector<char>(5));

    int k = 0;
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            matrix[i][j] = key[k++];
        }
    }

    return matrix;
}

string prepare_plaintext(string plaintext) {
    string text = "";

    for (char ch : plaintext) {
        if (isalpha(ch)) {
            ch = toupper(ch);
            if (ch == 'J')
                ch = 'I';
            text += ch;
        }
    }

    return text;
}

vector<string> create_digraphs(string plaintext) {
    vector<string> digraphs;
    int i = 0;

    while (i < plaintext.length()) {
        char first = plaintext[i];

        if (i + 1 >= plaintext.length()) {
            digraphs.push_back(string(1, first) + "X");
            i++;
        }
        else if (plaintext[i] == plaintext[i + 1]) {
            digraphs.push_back(string(1, first) + "X");
            i++;
        }
        else {
            digraphs.push_back(plaintext.substr(i, 2));
            i += 2;
        }
    }

    return digraphs;
}

pair<int, int> find_position(
    const vector<vector<char>>& matrix,
    char ch
) {
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            if (matrix[i][j] == ch)
                return {i, j};
        }
    }

    return {-1, -1};
}

string playfair_encrypt(
    const vector<string>& digraphs,
    const vector<vector<char>>& matrix
) {
    string ciphertext = "";

    for (string pair : digraphs) {
        auto p1 = find_position(matrix, pair[0]);
        auto p2 = find_position(matrix, pair[1]);

        int r1 = p1.first;
        int c1 = p1.second;
        int r2 = p2.first;
        int c2 = p2.second;

        if (r1 == r2) {
            ciphertext += matrix[r1][(c1 + 1) % 5];
            ciphertext += matrix[r2][(c2 + 1) % 5];
        }
        else if (c1 == c2) {
            ciphertext += matrix[(r1 + 1) % 5][c1];
            ciphertext += matrix[(r2 + 1) % 5][c2];
        }
        else {
            ciphertext += matrix[r1][c2];
            ciphertext += matrix[r2][c1];
        }
    }

    return ciphertext;
}

string playfair_decrypt(
    string ciphertext,
    const vector<vector<char>>& matrix
) {
    string plaintext = "";

    for (int i = 0; i < ciphertext.length(); i += 2) {
        char a = ciphertext[i];
        char b = ciphertext[i + 1];

        auto p1 = find_position(matrix, a);
        auto p2 = find_position(matrix, b);

        int r1 = p1.first;
        int c1 = p1.second;
        int r2 = p2.first;
        int c2 = p2.second;

        if (r1 == r2) {
            plaintext += matrix[r1][(c1 + 4) % 5];
            plaintext += matrix[r2][(c2 + 4) % 5];
        }
        else if (c1 == c2) {
            plaintext += matrix[(r1 + 4) % 5][c1];
            plaintext += matrix[(r2 + 4) % 5][c2];
        }
        else {
            plaintext += matrix[r1][c2];
            plaintext += matrix[r2][c1];
        }
    }

    return plaintext;
}

map<string, int> digraph_frequency(string ciphertext) {
    map<string, int> frequency;

    for (int i = 0; i < ciphertext.length(); i += 2) {
        string pair = ciphertext.substr(i, 2);
        frequency[pair]++;
    }

    return frequency;
}

bool verify(
    string ciphertext,
    const vector<vector<char>>& matrix
) {
    string decrypted = playfair_decrypt(ciphertext, matrix);
    vector<string> digraphs = create_digraphs(decrypted);
    string reencrypted = playfair_encrypt(digraphs, matrix);

    return reencrypted == ciphertext;
}

int main() {
    string keyword, plaintext;

    cout << "Keyword: ";
    cin >> keyword;

    cin.ignore();

    cout << "Plaintext: ";
    getline(cin, plaintext);

    vector<vector<char>> matrix =
        generate_key_matrix(keyword);

    cout << "\nKey Matrix\n";

    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            cout << matrix[i][j] << " ";
        }
        cout << endl;
    }

    string prepared = prepare_plaintext(plaintext);

    vector<string> digraphs =
        create_digraphs(prepared);

    cout << "\nPrepared Digraphs:\n";

    for (string pair : digraphs)
        cout << pair << " ";

    string ciphertext =
        playfair_encrypt(digraphs, matrix);

    cout << "\n\nCiphertext:\n";
    cout << ciphertext << endl;

    string decrypted =
        playfair_decrypt(ciphertext, matrix);

    cout << "\nDecrypted Text:\n";
    cout << decrypted << endl;

    map<string, int> frequency =
        digraph_frequency(ciphertext);

    cout << "\nDigraph Frequency Analysis:\n";

    for (auto entry : frequency) {
        cout << entry.first << ": "
             << entry.second << endl;
    }

    cout << "\nVerification:\n";

    if (verify(ciphertext, matrix))
        cout << "SUCCESS" << endl;
    else
        cout << "FAILED" << endl;

    return 0;
}

