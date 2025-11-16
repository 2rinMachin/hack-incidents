{
  pkgs ? import <nixpkgs> { },
}:
pkgs.mkShell {
  packages = with pkgs; [
    awscli2
    jq
    zip
    nodejs
    (python311.withPackages (ps: with ps; [ pip ]))
    serverless
  ];
}
