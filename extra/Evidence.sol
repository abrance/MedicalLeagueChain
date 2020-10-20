pragma solidity ^0.4.24;


contract Evidence{
    uint CODE_SUCCESS = 0;
    uint FILE_NOT_EXIST = 3002;
    uint FILE_ALREADY_EXIST  = 3003;

    event SaveEvent(uint returnValue,bytes filenameHash,bytes fileHash,uint fileUploadTime);

    struct FileEvidence{
        bytes filenameHash;
        bytes fileHash;
        uint fileUploadTime;
        address owner;
    }

    uint public evidenceCount;

    mapping(bytes => FileEvidence) fileEvidenceMap;

    function saveEvidence(bytes filenameHash,bytes fileHash,uint fileUploadTime) public payable returns(uint code){
        bytes memory keyHash = mergeBytes(filenameHash, fileHash);
        FileEvidence storage fileEvidence = fileEvidenceMap[keyHash];
        if(fileEvidence.fileHash.length != 0){
            (FILE_ALREADY_EXIST, "", "", 0);
            return FILE_ALREADY_EXIST;
        }

        evidenceCount += 1;
        fileEvidence.filenameHash = filenameHash;
        fileEvidence.fileHash = fileHash;
        fileEvidence.fileUploadTime = fileUploadTime;
        fileEvidence.owner = msg.sender;
        fileEvidenceMap[fileHash] = fileEvidence;

        emit SaveEvent(CODE_SUCCESS, filenameHash, fileHash, fileUploadTime);
        return CODE_SUCCESS;
    }
        
    function getEvidence(bytes filenameHash,bytes fileHash) public view returns(uint code,bytes fnHash,bytes fHash,uint fUpLoadTime,address saverAddress) {
        bytes memory keyHash = mergeBytes(filenameHash, fileHash);
        FileEvidence memory fileEvidence = fileEvidenceMap[keyHash];
        if(fileEvidence.fileHash.length == 0){
            return (FILE_NOT_EXIST,"","",0,msg.sender);
        }

        return(CODE_SUCCESS,fileEvidence.filenameHash,fileEvidence.fileHash,fileEvidence.fileUploadTime,msg.sender);
    }

    function mergeBytes(bytes param1, bytes param2) public pure returns (bytes) {
        bytes memory merged = new bytes(param1.length + param2.length);
        uint k = 0;
        for (uint i = 0; i < param1.length; i++) {
            merged[k] = param1[i];
            k++;
        }
        for (i = 0; i < param2.length; i++) {
            merged[k] = param2[i];
            k++;
        }
        return merged;
    }
}
