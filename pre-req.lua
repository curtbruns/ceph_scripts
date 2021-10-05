if Request.RGWOp == 'put_obj' then
	RGWDebugLog("Domain/URI/SC for put: " .. Request.HTTP.Domain .. " and URI: " .. Request.HTTP.URI .. " and StorageClass: " .. Request.HTTP.StorageClass)
  if (Request.HTTP.Metadata["x-amz-storage-class"] == nil) then
	  RGWDebugLog("No STORAGE CLASS Header for this Object put: " .. Request.Object.Name .. " Adding QLC_CLASS to MetaData and to HTTP request")
--	  Request.HTTP.Metadata["x-amz-storage-class"] = "QLC_CLASS"
--	  Request.HTTP.Metadata["x-amz-meta-mydata"] = "my value"
--	NewIndexClosure to allow mod for storage_class in HTTP Request
	  Request.HTTP.StorageClass = "QLC_CLASS"
		-- Should fail for unsupported field
--		Request.HTTP.URI = 'SomeHack'
  else
	  RGWDebugLog("Storage Class Header was sent on: " .. Request.Object.Name .. " and storage class: " .. Request.HTTP.Metadata["x-amz-storage-class"])
  end
  --RGWDebugLog("Now Headers: x-amz-meta-mydata " .. Request.HTTP.Metadata )
	for k, v in pairs(Request.HTTP.Metadata) do
	  RGWDebugLog("Pre-req Metadata key=" .. k .. ", " .. "value=" .. v)
	--RGWDebugLog("Storage Class Header avail on: " .. Request.Object.Name .. " and storage class: " .. Request.HTTP.Metadata["x-amz-storage-class"])
	end
	for k, v in pairs(Request.HTTP.Resources) do
	  RGWDebugLog("Pre-req Resources key=" .. k .. ", " .. "value=" .. v)
	--RGWDebugLog("Storage Class Header avail on: " .. Request.Object.Name .. " and storage class: " .. Request.HTTP.Metadata["x-amz-storage-class"])
	end
	for k, v in pairs(Request.HTTP.Parameters) do
	  RGWDebugLog("Pre-req Parameters key=" .. k .. ", " .. "value=" .. v)
	--RGWDebugLog("Storage Class Header avail on: " .. Request.Object.Name .. " and storage class: " .. Request.HTTP.Metadata["x-amz-storage-class"])
	end

	-- Dump the request table - can't its not iterable
--	for k, v in pairs(Request.HTTP) do
--		RGWDebugLog("Request HTTP key=" .. k .. ", " .. "value=" .. v)
--	end

end

