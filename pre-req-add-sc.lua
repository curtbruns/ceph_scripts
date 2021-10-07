local function isempty(input)
  return input == nil or input == ''
end

if Request.RGWOp == 'put_obj' then
	RGWDebugLog("Host/Domain/URI/SC for put Host: " .. Request.HTTP.Host .. " Domain: " .. Request.HTTP.Domain .. " URI: " .. Request.HTTP.URI .. " and StorageClass: " .. Request.HTTP.StorageClass )
  if (isempty(Request.HTTP.StorageClass)) then
	  RGWDebugLog("No StorageClass for this Object put: " .. Request.Object.Name .. " Adding QLC_CLASS to HTTP request")
	  Request.HTTP.StorageClass = "QLC_CLASS"
  else
	  RGWDebugLog("Storage Class Header was sent on: " .. Request.Object.Name .. " and storage class: " .. Request.HTTP.StorageClass)
  end
end

