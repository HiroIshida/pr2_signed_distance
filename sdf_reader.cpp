#include <fstream>
#include <string>
#include <iostream>
#include <vector>
#define print(something) std::cout<< something <<std::endl;

using tensor3 = std::vector<std::vector<std::vector<float>>>;
using namespace std;

class SignedDistanceField
{
  public:
    SignedDistanceField(string filename);
    float compute_sd(vector<float> point);

    tensor3 data;
    vector<int> Nxyz;
    vector<float> dxyz;

  private:
    vector<int> where_am_i(vector<float> point);
};

SignedDistanceField::SignedDistanceField(string filename){
  ifstream infile(filename);
  string line;
  getline(infile, line);
  int Nx, Ny, Nz, N;
  float dx, dy, dz;
  sscanf(line.data(), "%d %d %d", &Nx, &Ny, &Nz);
  N = Nx*Ny*Nz;
  getline(infile, line);
  sscanf(line.data(), "%f %f %f", &dx, &dy, &dz);

  float value;
  vector<float> data_raw;
  while(getline(infile, line)){
    getline(infile, line);
    sscanf(line.data(), "%f", &value);
    data_raw.push_back(value);
  }

  tensor3 data_;
  for(int i = 0; i < Nx; i++){
    vector<vector<float>> vec_j;
    for(int j = 0; j < Ny; j++){
      vector<float> vec_k;
      for(int k = 0; k < Nz; k++){
        int idx = i + Nx * j + Nx * Ny * k;
        vec_k.push_back(data_raw[idx]);
      }
      vec_j.push_back(vec_k);
    }
    data_.push_back(vec_j);
  }
  vector<int> Nxyz_{Nx, Ny, Nz};
  vector<float> dxyz_{dx, dy, dz};

  // initialization
  data = data_;
  Nxyz = Nxyz_;
  dxyz = dxyz_;
}

float signed_distance(vector<float> point, tensor3 sdf){
}

vector<int> where_am_i(vector<float> point){
}

int main(){
}

