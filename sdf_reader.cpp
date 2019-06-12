#include <fstream>
#include <string>
#include <iostream>
#include <vector>
#include"./third/json/single_include/nlohmann/json.hpp"
#define print(something) std::cout<< something <<std::endl;

using array3d = std::vector<std::vector<std::vector<float>>>;
using namespace std;

class SignedDistanceField
{
  public:
    SignedDistanceField(string filename);
    float compute_sd(vector<float> point);
    void dump_json();

    array3d data;
    vector<int> Nxyz;
    vector<float> bmin;
    float dx;

  private:
    vector<int> where_am_i(vector<float> point);
};

SignedDistanceField::SignedDistanceField(string filename){
  ifstream infile(filename);
  string line;
  getline(infile, line);
  int Nx, Ny, Nz;
  sscanf(line.data(), "%d %d %d", &Nx, &Ny, &Nz);

  float bmin_x, bmin_y, bmin_z;
  getline(infile, line);
  sscanf(line.data(), "%f %f %f", &bmin_x, &bmin_y, &bmin_z);

  float dx_;
  getline(infile, line);
  sscanf(line.data(), "%f", &dx_);


  float value;
  vector<float> data_raw;
  while(getline(infile, line)){
    getline(infile, line);
    sscanf(line.data(), "%f", &value);
    data_raw.push_back(value);
  }

  array3d data_;
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
  vector<float> bmin_{bmin_x, bmin_y, bmin_z};

  // initialization
  data = data_;
  Nxyz = Nxyz_;
  bmin = bmin_;
  dx = dx_;
}

void SignedDistanceField::dump_json(){
  nlohmann::json j;
  j["Nxyz"] = Nxyz;
  j["bmin"] = bmin;
  j["dx"] = dx;
  j["data"] = data;
  string filename = "./tmp.json";
  ofstream ofs(filename.c_str());
  ofs<<j<<endl;
}

int main(){
  SignedDistanceField sdf("sdffiles/gripper_palm.sdf");
  sdf.dump_json();
}

