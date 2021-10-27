local function isempty(input)
  return input == nil or input == ''
end

if Request.RGWOp == 'put_obj' then
	RGWDebugLog("Put_Obj with StorageClass: " .. Request.HTTP.StorageClass )
  if (isempty(Request.HTTP.StorageClass)) then
	  RGWDebugLog("No StorageClass for Object: " .. Request.Object.Name .. "  Adding StorageClass to HTTP request")
	  Request.HTTP.StorageClass = "QLC_CLASS"
  else
	  RGWDebugLog("Storage Class Header Present on Object: " .. Request.Object.Name .. " with StorageClass: " .. Request.HTTP.StorageClass)
  end
end

