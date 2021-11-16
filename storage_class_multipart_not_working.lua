local function isempty(input)
  return input == nil or input == ''
end

if Request.RGWOp == 'put_obj' then
  RGWDebugLog("Put_Obj with StorageClass: " .. Request.HTTP.StorageClass )
  if (isempty(Request.HTTP.StorageClass)) then
		if (Request.HTTP.Resources.partNumber) then
      RGWDebugLog("MultiPart Upload: " .. Request.Object.Name .. " and part: " .. Request.HTTP.Resources.partNumber .. " adding StorageClass")
      Request.HTTP.StorageClass = "QLC_CLASS"
		elseif (Request.ContentLength >= 65536) then
      RGWDebugLog("No StorageClass for Object and size > threshold: " .. Request.Object.Name .. " adding StorageClass")
      Request.HTTP.StorageClass = "QLC_CLASS"
    end
  else
    RGWDebugLog("Storage Class Header Present on Object: " .. Request.Object.Name .. " with StorageClass: " .. Request.HTTP.StorageClass)
  end
elseif Request.RGWOp == 'init_multipart' then 
	if isempty(Request.HTTP.StorageClass) then
      RGWDebugLog("MultiPart Upload Starting w/o StorageClass, adding StorageClass")
      Request.HTTP.StorageClass = "QLC_CLASS"
  else 
      RGWDebugLog("MultiPart Upload has StorageClass: " .. Request.HTTP.StorageClass)
  end
end

